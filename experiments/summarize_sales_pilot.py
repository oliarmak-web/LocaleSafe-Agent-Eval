"""Audit frozen draft enterprise-sales pilot runs without model dependencies."""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from localesafe.collect_sales_pilot import ordered_jobs, SOURCES, MODELS
from localesafe.evaluate import read_jsonl, sha256
from localesafe.sales_pilot import messages_for, score, seed_for, cases as frozen_cases, LANGUAGES, PROFILES, unsupported


def audit(directory):
    manifest = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
    if manifest['status'] != 'completed':
        raise ValueError('incomplete collection')
    hashes = json.loads((directory / 'archive-sha256.json').read_text(encoding='utf-8'))
    actual = {p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file() and p.name != 'archive-sha256.json'}
    if set(hashes) != actual:
        raise ValueError('archive inventory mismatch')
    for relative, digest in hashes.items():
        path = (directory / relative).resolve()
        if not path.is_relative_to(directory.resolve()) or sha256(path) != digest:
            raise ValueError('archive hash mismatch')
    if sha256(directory / 'attempts.jsonl') != manifest['attempts_sha256'] or sha256(directory / 'cases.jsonl') != manifest['cases_sha256']:
        raise ValueError('artifact hash mismatch')
    settings = manifest['settings']
    if (set(settings['sources']) != set(SOURCES) or settings['model'] not in MODELS.values()
        or settings['split'] != 'development' or settings['batch_size'] != 8
        or settings['dtype'] != 'float16' or settings['quantization'] != 'none'
        or settings['enable_thinking'] is not False
        or settings['token_limits'] != {'extract':128,'qualify_history':96,'qualify_oracle':96,'qualify_generated':96}):
        raise ValueError('unexpected pilot configuration')
    if sha256(directory / 'design.json') != settings['design_sha256']:
        raise ValueError('design hash mismatch')
    for name, digest in settings['sources'].items():
        if sha256(directory / 'source' / name) != digest:
            raise ValueError('source hash mismatch')
    cases, rows = read_jsonl(directory / 'cases.jsonl'), read_jsonl(directory / 'attempts.jsonl')
    if cases != frozen_cases() or settings['profiles'] != list(PROFILES) or settings['seed'] != 20261023:
        raise ValueError('frozen pilot grid mismatch')
    # Collector serializes selected cases on Linux; the frozen source may use
    # Windows line endings. Verify both complete wire forms without editing data.
    case_bytes=(directory/'cases.jsonl').read_bytes().replace(b'\r\n',b'\n')
    source_forms={hashlib.sha256(case_bytes).hexdigest(),hashlib.sha256(case_bytes.replace(b'\n',b'\r\n')).hexdigest()}
    if settings['all_cases_sha256'] not in source_forms:
        raise ValueError('source cases mismatch')
    indexed = {c['id']: c for c in cases}
    design = json.loads((directory / 'design.json').read_text(encoding='utf-8'))
    if any(design[c['id']]['split'] != settings['split'] for c in cases):
        raise ValueError('split mismatch')
    jobs = ordered_jobs(cases, settings['profiles'], settings['seed'])
    if len(rows) != len(jobs) or len(rows) != manifest['attempts'] or len(rows) != manifest['scheduled_requests']:
        raise ValueError('incomplete request grid')
    previous = {}
    for row, job in zip(rows, jobs):
        case = indexed[job['case_id']]
        if row['job'] != job or row['messages'] != messages_for(case, job, previous):
            raise ValueError('job/prompt mismatch')
        if row['scores'] != score(case, job, row['raw_output']) or row['seed'] != seed_for(case, job):
            raise ValueError('score/seed mismatch')
        if type(row['output_tokens']) is not int or not 0 < row['output_tokens'] <= settings['token_limits'][job['stage']]:
            raise ValueError('invalid output token count')
        previous[job['id']] = row
    return manifest, cases, rows


def summarize(manifest, cases, rows):
    indexed={c['id']:c for c in cases}
    groups=defaultdict(list)
    by_cell={}
    for row in rows:
        j=row['job']
        c=indexed[j['case_id']]
        groups[(j['stage'],j['profile'],c['language'])].append(row)
        by_cell[(c['family'],c['language'],j['profile'],j['stage'])]=row
    counts=[]
    for (stage,profile,language), group in sorted(groups.items()):
        item={'stage':stage,'profile':profile,'language':language,'requests':len(group),
              'parsed':sum(r['scores']['parsed'] for r in group),'correct':sum(r['scores']['correct'] for r in group),
              'token_limit_hits':sum(r['output_tokens']==manifest['settings']['token_limits'][stage] for r in group)}
        if stage=='extract':
            item['fields']={k:sum(r['scores']['fields'][k] for r in group) for k in group[0]['scores']['fields']}
        else:
            item.update({k:sum(r['scores'][k] for r in group) for k in
                        ('decision_correct','unsupported_fit_claim','unnecessary_escalation')})
            item['unsupported_cases']=sum(bool(unsupported(indexed[r['job']['case_id']]['requirements'])) for r in group)
            item['all_supported_cases']=len(group)-item['unsupported_cases']
        counts.append(item)
    pairs=[]
    families=sorted({c['family'] for c in cases})
    stages=('extract','qualify_history','qualify_oracle','qualify_generated')
    for language in LANGUAGES[1:]:
        for profile in PROFILES:
            for stage in stages:
                lost,gained=[],[]
                for family in families:
                    en=by_cell[(family,'en',profile,stage)]['scores']['correct']
                    other=by_cell[(family,language,profile,stage)]['scores']['correct']
                    if en and not other: lost.append(family)
                    if other and not en: gained.append(family)
                pairs.append({'language':language,'profile':profile,'stage':stage,'n':len(families),
                              'english_correct_other_wrong':lost,'other_correct_english_wrong':gained})
    repeats=[]
    for language in LANGUAGES:
        for stage in stages:
            a=[by_cell[(f,language,'sample-1',stage)] for f in families]
            b=[by_cell[(f,language,'sample-2',stage)] for f in families]
            repeats.append({'language':language,'stage':stage,'n':len(families),
                            'raw_disagreements':sum(x['raw_output']!=y['raw_output'] for x,y in zip(a,b)),
                            'correctness_disagreements':sum(x['scores']['correct']!=y['scores']['correct'] for x,y in zip(a,b))})
    return {'model':manifest['settings']['model']['model'],'review_status':'AI-authored-draft',
            'requests':len(rows),'families':len(families),'cases':len(cases),'groups':counts,
            'paired_vs_english':pairs,'sampled_repeats':repeats,'attempts_sha256':manifest['attempts_sha256']}


def render(results):
    lines=['# Draft enterprise-sales discovery pilot', '',
           '**Unreviewed feasibility results.** Fictional product, six situation templates, five languages. No real buyers, revenue, outbound proposals or production-safety claims.', '',
           '## Greedy results', '',
           '| Model | Buyer language | Requirements correct | Fit from conversation | Fit from reference | Fit from extraction | Unsupported fit claims from conversation |',
           '|---|---|---:|---:|---:|---:|---:|']
    for result in results:
        for language in LANGUAGES:
            g={x['stage']:x for x in result['groups'] if x['profile']=='greedy' and x['language']==language}
            cells=[f"{g[stage]['correct']}/{g[stage]['requests']}" for stage in ('extract','qualify_history','qualify_oracle','qualify_generated')]
            claims=f"{g['qualify_history']['unsupported_fit_claim']}/{g['qualify_history']['unsupported_cases']}"
            lines.append(f"| {result['model']} | {language} | "+' | '.join(cells)+f" | {claims} |")
    lines += ['', 'Extraction checks five requirement fields. Fit correctness requires both the right decision and the complete unsupported-field list. Invalid outputs count as failures; they are not safe decisions.', '',
              'The oracle supplies English-keyed correct requirements rather than the buyer conversation. Its language labels identify matched cases, not language present in the oracle prompt. Generated-record assessment consumes the exact retained extraction, including malformed text.', '',
              'All sampled profiles, within-language repeat disagreements and matched English contrasts are retained in the JSON. Do not pool them as independent scenarios. No significance test, model competence gate, held-out evaluation or causal language ranking is supported. A zero field score after failed parsing does not prove semantic loss.', '',
              'Independent language/domain review, native-authored paraphrases, more situation families and untouched evaluation cases are outstanding. These results assess internal discovery and fit only; they do not validate complete enterprise-sales agents.', '',
              '[Frozen protocol](../experiments/sales-pilot/PROTOCOL.md).']
    return '\n'.join(lines)+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directories',nargs='+',type=Path)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    results=[summarize(*audit(path)) for path in args.directories]
    args.output_dir.mkdir(parents=True,exist_ok=False)
    (args.output_dir/'summary.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    (args.output_dir/'RESULTS.md').write_text(render(results),encoding='utf-8')


if __name__=='__main__':
    main()

