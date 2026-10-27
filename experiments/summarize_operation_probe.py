"""Audit counterbalanced operation choices and compare the narrower parent task."""
import argparse
from collections import Counter
import json
from pathlib import Path
import random

from experiments.build_hindi_pair import build, PATTERNS
from experiments.summarize_hindi_pair import analyze as audit_parent
from localesafe.collect_handoff import MODELS
from localesafe.collect_operation_probe import SOURCES
from localesafe.evaluate import read_jsonl,sha256
from localesafe.operation_probe import jobs_for,messages_for,score,ORDERS


def analyze(directory,parent):
    hashes=json.loads((directory/'archive-sha256.json').read_text(encoding='utf-8'))
    inventory={p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file() and p.name!='archive-sha256.json'}
    if set(hashes)!=inventory:raise ValueError('Inventory mismatch')
    for name,digest in hashes.items():
        path=(directory/name).resolve()
        if not path.is_relative_to(directory.resolve()) or sha256(path)!=digest:raise ValueError('Archive hash/path mismatch')
    manifest=json.loads((directory/'manifest.json').read_text(encoding='utf-8'));s=manifest['settings']
    if manifest['status']!='completed' or manifest['attempts']!=336 or manifest['scheduled_requests']!=336:
        raise ValueError('Incomplete run')
    if (s['model']!=MODELS['qwen3-4b'] or s['decoding']!='greedy' or s['max_new_tokens']!=8
        or s['schedule_seed']!=20261027 or s['dtype']!='float16' or s['quantization']!='none'
        or s['batch_size']!=8 or s['threads']!=2 or s['enable_thinking'] is not False
        or s['transformers']!='4.57.6' or 'T4' not in s['gpu'] or set(s['sources'])!=set(SOURCES)):
        raise ValueError('Frozen settings mismatch')
    for name,digest in s['sources'].items():
        if sha256(directory/'source'/name)!=digest:raise ValueError('Source hash mismatch')
    for name in ('cases','jobs'):
        if sha256(directory/(name+'.json'))!=s[name+'_sha256']:raise ValueError('Input hash mismatch')
    cases=json.loads((directory/'cases.json').read_text(encoding='utf-8'))
    expected,_=build()
    if cases!=expected:raise ValueError('Frozen case mismatch')
    jobs=json.loads((directory/'jobs.json').read_text(encoding='utf-8'))
    if jobs!=jobs_for(cases):raise ValueError('Frozen job mismatch')
    random.Random(20261027).shuffle(jobs)
    rows=read_jsonl(directory/'attempts.jsonl')
    if len(rows)!=336 or sha256(directory/'attempts.jsonl')!=manifest['attempts_sha256']:raise ValueError('Attempt count/hash mismatch')
    indexed={c['id']:c for c in cases}
    for job,row in zip(jobs,rows):
        case=indexed[job['case_id']]
        if row['job']!=job or row['messages']!=messages_for(case,job) or row['scores']!=score(case,job,row['raw_output']):
            raise ValueError('Job/prompt/score mismatch')
        if type(row['output_tokens']) is not int or not 0<row['output_tokens']<=8:raise ValueError('Token count mismatch')
        if len(row['prompt_sha256'])!=64 or any(x not in '0123456789abcdef' for x in row['prompt_sha256']):
            raise ValueError('Invalid prompt hash')
    parent_summary=audit_parent(parent)
    parent_rows=read_jsonl(parent/'attempts.jsonl')
    original={r['job']['case_id']:r for r in parent_rows if r['job']['stage']=='actor'
              and r['job']['condition']=='full_history' and r['job']['profile']=='greedy'}
    groups=[]
    by_case={c['id']:[r for r in rows if r['job']['case_id']==c['id']] for c in cases}
    comparisons=[]
    for pattern in PATTERNS:
        subset=[r for r in rows if indexed[r['job']['case_id']]['language_pattern']==pattern]
        ids=[c['id'] for c in cases if c['language_pattern']==pattern]
        all_correct=[cid for cid in ids if all(r['scores']['correct'] for r in by_case[cid])]
        sensitivity=[cid for cid in ids if len({r['scores']['correct'] for r in by_case[cid]})>1]
        letters={letter:{'correct':sum(r['scores']['correct'] for r in subset if r['scores']['reference_letter']==letter),
                         'n':sum(r['scores']['reference_letter']==letter for r in subset)} for letter in 'ABC'}
        groups.append({'pattern':pattern,'requests':len(subset),'valid':sum(r['scores']['valid_letter'] for r in subset),
                       'correct':sum(r['scores']['correct'] for r in subset),'cases':len(ids),
                       'all_orders_correct':all_correct,'order_sensitive_correctness':sensitivity,
                       'selected_letters':dict(Counter(r['raw_output'] if r['scores']['valid_letter'] else 'invalid' for r in subset)),
                       'accuracy_by_reference_letter':letters,
                       'parent_actor_correct':sum(original[cid]['scores']['correct'] for cid in ids)})
        comparisons.append({'pattern':pattern,
                            'parent_wrong_probe_all_orders_right':[cid for cid in all_correct if not original[cid]['scores']['correct']],
                            'parent_right_probe_not_all_orders_right':[cid for cid in ids if original[cid]['scores']['correct'] and cid not in all_correct]})
    orders=[]
    for pattern in PATTERNS:
        for order in ORDERS:
            subset=[r for r in rows if indexed[r['job']['case_id']]['language_pattern']==pattern and r['job']['order']==list(order)]
            orders.append({'pattern':pattern,'order':list(order),'correct':sum(r['scores']['correct'] for r in subset),'n':len(subset)})
    return {'requests':336,'cases':56,'templates':4,'groups':groups,'order_groups':orders,
            'changed_task_comparisons':comparisons,'manifest_sha256':sha256(directory/'manifest.json'),
            'parent_attempts_sha256':sha256(parent/'attempts.jsonl'),'parent_english_gate':parent_summary['summary']['english_gate']}


def render(result):
    lines=['# Requested-operation probe: results','',
           '336 greedy calls; the same 56 draft cases, each tested under all six A/B/C option orders. This identifies wait/propose/commit only; it does not execute an action or test exact arguments, authorization or final state.','',
           '| Pattern | Valid letters | Correct choices | Cases correct under all six orders | Order-sensitive cases | Parent full-action score |',
           '|---|---:|---:|---:|---:|---:|']
    for r in result['groups']:
        lines.append(f"| {r['pattern']} | {r['valid']}/{r['requests']} | {r['correct']}/{r['requests']} | {len(r['all_orders_correct'])}/{r['cases']} | {len(r['order_sensitive_correctness'])}/{r['cases']} | {r['parent_actor_correct']}/{r['cases']} |")
    lines+=['','All six permutations give each reference answer letter twice per case. The 48 choices per language pattern are repeated measurements on eight situation/variant rows, not 48 independent situations.','',
            'The parent action score includes target, value and version; this probe changes the prompt and output task. The narrower choice score cannot replace the full-action score or establish language comprehension.','',
            '## Accuracy by correct answer position','', '| Pattern | A | B | C |','|---|---:|---:|---:|']
    for r in result['groups']:
        cells=[f"{r['accuracy_by_reference_letter'][x]['correct']}/{r['accuracy_by_reference_letter'][x]['n']}" for x in 'ABC']
        lines.append('| '+r['pattern']+' | '+' | '.join(cells)+' |')
    lines+=['','Designed after inspecting parent errors. Hindi and Spanish text lack independent review; there is no held-out evaluation or significance claim. See the machine-readable summary for per-order counts, selected-letter counts and individual changed-task comparisons.']
    return '\n'.join(lines)+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--parent',type=Path,default=Path('experiments/results/hindi-pair-qwen3-4b-20261027'))
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args();result=analyze(args.directory,args.parent)
    args.output_dir.mkdir(parents=True,exist_ok=False)
    (args.output_dir/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (args.output_dir/'RESULTS.md').write_text(render(result),encoding='utf-8')
    print(json.dumps({'calls':result['requests'],'cases':result['cases']}))


if __name__=='__main__':main()
