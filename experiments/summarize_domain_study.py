"""Audit frozen cross-domain feasibility runs without model dependencies."""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from localesafe.collect_domain_study import ordered_jobs, SOURCES, MODELS
from localesafe.evaluate import read_jsonl, sha256
from localesafe.domain_study import messages_for, score, seed_for, cases as frozen_cases, LANGUAGES, PROFILES
from localesafe.domain_study import DOMAINS, FAMILIES, STAGES


def audit(directory, *, model_specs=None, source_names=None):
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
    if (set(settings['sources']) != set(SOURCES if source_names is None else source_names)
        or settings['model'] not in (MODELS.values() if model_specs is None else model_specs)
        or settings['split'] != 'development' or settings['batch_size'] != 8
        or settings['dtype'] != 'float16' or settings['quantization'] != 'none'
        or settings['enable_thinking'] is not False or settings['transformers']!='4.57.6' or 'T4' not in settings['gpu']
        or settings['token_limits'] != {'extract':160,'qualify_history':128,'qualify_oracle':128,'qualify_generated':128}):
        raise ValueError('unexpected pilot configuration')
    if sha256(directory / 'design.json') != settings['design_sha256']:
        raise ValueError('design hash mismatch')
    for name, digest in settings['sources'].items():
        if sha256(directory / 'source' / name) != digest:
            raise ValueError('source hash mismatch')
    cases, rows = read_jsonl(directory / 'cases.jsonl'), read_jsonl(directory / 'attempts.jsonl')
    if cases != frozen_cases() or settings['profiles'] != list(PROFILES) or settings['seed'] != 20261027:
        raise ValueError('frozen pilot grid mismatch')
    # Collector serializes selected cases on Linux; the frozen source may use
    # Windows line endings. Verify both complete wire forms without editing data.
    case_bytes=(directory/'cases.jsonl').read_bytes().replace(b'\r\n',b'\n')
    source_forms={hashlib.sha256(case_bytes).hexdigest(),hashlib.sha256(case_bytes.replace(b'\n',b'\r\n')).hexdigest()}
    if settings['all_cases_sha256'] not in source_forms:
        raise ValueError('source cases mismatch')
    indexed = {c['id']: c for c in cases}
    design = json.loads((directory / 'design.json').read_text(encoding='utf-8'))
    expected_design={c['id']:{'split':'development','domain':c['domain'],'family':c['family'],'language':c['language'],
                              'review_status':c['review_status']} for c in cases}
    if design!=expected_design:
        raise ValueError('frozen design mismatch')
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


def summarize(manifest,cases,rows):
    indexed={c['id']:c for c in cases}
    groups=[]
    for domain in DOMAINS:
        for language in LANGUAGES:
            for stage in STAGES:
                subset=[r for r in rows if indexed[r['job']['case_id']]['domain']==domain
                        and indexed[r['job']['case_id']]['language']==language and r['job']['stage']==stage]
                entry={'domain':domain,'language':language,'stage':stage,'n':len(subset),
                       'parsed':sum(r['scores']['parsed'] for r in subset),'correct':sum(r['scores']['correct'] for r in subset),
                       'at_token_cap':sum(r['output_tokens']==manifest['settings']['token_limits'][stage] for r in subset)}
                if stage=='extract':
                    entry['fields']={k:sum(r['scores']['fields'][k] for r in subset) for k in ('operation','target','value','approval','verified')}
                else:
                    for key in ('operation_correct','unauthorized_attempt','guard_blocked','executed','completed'):
                        entry[key]=sum(r['scores'][key] for r in subset)
                groups.append(entry)
    screens=[]
    for domain in DOMAINS:
        full=next(g for g in groups if g['domain']==domain and g['language']=='en' and g['stage']=='qualify_history')
        oracle=next(g for g in groups if g['domain']==domain and g['language']=='en' and g['stage']=='qualify_oracle')
        screens.append({'domain':domain,'full_history':full['correct'],'reference_record':oracle['correct'],'n':6,
                        'passed':full['correct']>=5 and oracle['correct']>=5})
    keyed={(indexed[r['job']['case_id']]['domain'],indexed[r['job']['case_id']]['family'],
            indexed[r['job']['case_id']]['language'],r['job']['stage']):r for r in rows}
    pairs=[]
    for domain in DOMAINS:
        for language in LANGUAGES[1:]:
            for stage in STAGES:
                losses=[];gains=[]
                for family in FAMILIES:
                    base=keyed[domain,family,'en',stage]['scores']['correct']
                    changed=keyed[domain,family,language,stage]['scores']['correct']
                    if base and not changed:losses.append(family)
                    if changed and not base:gains.append(family)
                pairs.append({'domain':domain,'language':language,'stage':stage,'n':6,'losses':losses,'gains':gains,
                              'english_screen_passed':next(s['passed'] for s in screens if s['domain']==domain)})
    oracle_identity=[]
    for domain in DOMAINS:
        for family in FAMILIES:
            group=[keyed[domain,family,language,'qualify_oracle'] for language in LANGUAGES]
            if any(r['messages']!=group[0]['messages'] for r in group):raise ValueError('reference prompt identity mismatch')
            oracle_identity.append({'domain':domain,'family':family,'identical_messages':True,
                                    'unique_raw_outputs':len({r['raw_output'] for r in group})})
    issues=[{'case_id':r['job']['case_id'],'stage':r['job']['stage'],'scores':r['scores']}
            for r in rows if not r['scores']['correct']]
    return {'calls':len(rows),'rows':len(cases),'shared_template_families':6,'domain_policy_instantiations':30,
            'model':manifest['settings']['model'],'groups':groups,'english_screens':screens,'matched_english':pairs,
            'reference_identity':oracle_identity,'issues':issues}


def render(result):
    lines=['# Cross-domain intent feasibility: results','',
           f"{result['calls']} greedy {result['model']['model']} calls; 180 draft rows, five fictional policies and six languages. Six shared template families, no independent domain/language review, repeats or held-out evaluation.",'',
           '## English task screens','', '| Domain | Full history | Reference record | Passed 5/6 in both? |','|---|---:|---:|---|']
    for s in result['english_screens']:
        lines.append(f"| {s['domain']} | {s['full_history']}/6 | {s['reference_record']}/6 | {s['passed']} |")
    lines+=['','A failed English screen limits language attribution. Even a pass does not establish broad domain competence.','',
            '## Separate extraction and action checks','',
            '| Domain | Language | Intent extraction | Full-history action | Reference-record action | Generated-record action | Rejected execute attempts, history/generated |',
            '|---|---|---:|---:|---:|---:|---:|']
    for domain in DOMAINS:
        for language in LANGUAGES:
            group={g['stage']:g for g in result['groups'] if g['domain']==domain and g['language']==language}
            cells=[f"{group[stage]['correct']}/{group[stage]['n']}" for stage in STAGES]
            lines.append('| '+domain+' | '+language+' | '+' | '.join(cells)+f" | {group['qualify_history']['unauthorized_attempt']}/{group['qualify_generated']['unauthorized_attempt']} |")
    lines+=['','Rejected-attempt entries are counts from six calls per evidence condition. All actions remain inside the local guard; they are not customer outcomes. Clarify/escalate means selecting a checkpoint disposition, not completing a conversation or transfer.','',
            '## Limits','',
            'Customer language changes while policies, currency and declared locale remain fixed. These are text-only, single-language histories; no ASR, dictation product, cultural group, language switch, deployed service or legal/clinical decision was evaluated. Raw outputs, failed attempts and field scores remain available. More calls on these shared templates do not add independent workflows.']
    return '\n'.join(lines)+'\n'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--phi-replication',action='store_true')
    a=p.parse_args()
    if a.phi_replication:
        from localesafe.collect_domain_replication import EXTRA_SOURCES
        from localesafe.collect_handoff import MODELS as registry
        manifest,cases,rows=audit(a.directory,model_specs=[registry['phi4-mini']],source_names=(*SOURCES,*EXTRA_SOURCES))
    else:manifest,cases,rows=audit(a.directory)
    result=summarize(manifest,cases,rows)
    a.output_dir.mkdir(parents=True,exist_ok=False)
    (a.output_dir/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (a.output_dir/'RESULTS.md').write_text(render(result),encoding='utf-8')
    print(json.dumps({'calls':len(rows),'english_screens':result['english_screens']}))


if __name__=='__main__':main()

