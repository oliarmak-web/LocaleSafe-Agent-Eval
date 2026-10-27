"""Recompute the frozen switch-location control without model dependencies."""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path

from experiments.build_switch_boundary import build, LAYOUTS
from experiments.summarize_handoff import audit, summarize
from localesafe.collect_handoff import MODELS, SOURCES
from localesafe.collect_switch_boundary import ordered_jobs, EXTRA_SOURCES
from localesafe.evaluate import sha256


def analyze(directory):
    hashes=json.loads((directory/'archive-sha256.json').read_text(encoding='utf-8'))
    inventory={p.relative_to(directory).as_posix() for p in directory.rglob('*')
               if p.is_file() and p.name!='archive-sha256.json'}
    if inventory!=set(hashes):raise ValueError('Archive inventory mismatch')
    manifest,cases,rows=audit(directory,job_builder=ordered_jobs)
    expected,design=build()
    if cases!=expected or json.loads((directory/'design.json').read_text(encoding='utf-8'))!=design:
        raise ValueError('Frozen boundary grid mismatch')
    settings=manifest['settings']
    if (settings['model']!=MODELS['qwen3-4b'] or settings['split']!='development'
        or settings['profiles']!=['greedy','sample-1','sample-2'] or settings['seed']!=20261022
        or settings['dtype']!='float16' or settings['quantization']!='none' or settings['batch_size']!=8
        or settings['transformers']!='4.57.6' or 'T4' not in settings['gpu']
        or settings['enable_thinking'] is not False
        or settings['temperature']!=.7 or settings['top_p']!=.8 or settings['top_k']!=20
        or settings['token_limits']!={'summary':192,'actor':96,'monitor':24}
        or set(settings['sources'])!=set((*SOURCES,*EXTRA_SOURCES))):
        raise ValueError('Frozen settings mismatch')
    lf=(directory/'cases.jsonl').read_bytes().replace(b'\r\n',b'\n')
    if settings['all_cases_sha256'] not in {hashlib.sha256(lf).hexdigest(),hashlib.sha256(lf.replace(b'\n',b'\r\n')).hexdigest()}:
        raise ValueError('Input case hash mismatch')
    indexed={c['id']:c for c in cases}
    keyed={(indexed[r['job']['case_id']]['scenario'],indexed[r['job']['case_id']]['language_pattern'],
            r['job']['stage'],r['job']['condition'],r['job']['profile']):r for r in rows}
    scenarios=sorted({c['scenario'] for c in cases})
    pairs=[]
    for partner in ('es','hi'):
        switches=[f'en-{partner}-{location}' for location in ('before','at','after')]
        pairs.extend((baseline,layout) for baseline in ('en-en',f'{partner}-{partner}') for layout in switches)
        pairs.extend(combinations(switches,2))
    comparisons=[]
    for baseline,condition in pairs:
        losses=[];gains=[]
        for scenario in scenarios:
            ref=keyed[scenario,baseline,'actor','full_history','greedy']['scores']['correct']
            changed=keyed[scenario,condition,'actor','full_history','greedy']['scores']['correct']
            if ref and not changed:losses.append(scenario)
            if changed and not ref:gains.append(scenario)
        comparisons.append({'baseline':baseline,'condition':condition,'blocks':len(scenarios),'losses':losses,'gains':gains})
    repeats=[]
    for layout in LAYOUTS:
        for condition in ('full_history','oracle_record','generated_record'):
            changed=[s for s in scenarios if keyed[s,layout,'actor',condition,'sample-1']['scores']['correct']
                     !=keyed[s,layout,'actor',condition,'sample-2']['scores']['correct']]
            repeats.append({'layout':layout,'condition':condition,'blocks':len(scenarios),'correctness_changed':changed})
    oracle_checks=[]
    for scenario in scenarios:
        group=[keyed[scenario,layout,'actor','oracle_record','greedy'] for layout in LAYOUTS]
        if any(r['messages']!=group[0]['messages'] for r in group):raise ValueError('Oracle prompt differs across layouts')
        oracle_checks.append({'scenario':scenario,'prompts_identical':True,
                              'unique_greedy_raw_outputs':len({r['raw_output'] for r in group}),
                              'unique_greedy_correctness':len({r['scores']['correct'] for r in group})})
    fidelity=[]
    for layout in LAYOUTS:
        group=[r for r in rows if indexed[r['job']['case_id']]['language_pattern']==layout and r['job']['stage']=='summary']
        fidelity.append({'layout':layout,'records':len(group),'exact':sum(r['scores']['fidelity'] for r in group),
                         'fields':{key:sum(r['scores']['fields'][key] for r in group)
                                   for key in ('principal','version','source_event','permission','requested_action')}})
    return {'summary':summarize(manifest,cases,rows),'matched_greedy_comparisons':comparisons,
            'sampled_repeat_changes':repeats,'oracle_identity_checks':oracle_checks,
            'fidelity_by_layout':fidelity,'manifest_sha256':sha256(directory/'manifest.json')}


def render(result):
    summary=result['summary']
    lines=['# Language-switch location: results','',
           f"{summary['requests']} Qwen3-4B calls on 72 four-turn draft rows from four templates. No independent language review, held-out evaluation or audio.",'',
           '## Greedy action correctness','',
           '| Layout | Full history | Reference record | Generated record |','|---|---:|---:|---:|']
    for layout in LAYOUTS:
        cells=[]
        for condition in ('full_history','oracle_record','generated_record'):
            r=next(r for r in summary['actor'] if r['language_pattern']==layout and r['condition']==condition and r['profile']=='greedy')
            cells.append(f"{r['correct']}/{r['requests']}")
        lines.append('| '+layout+' | '+' | '.join(cells)+' |')
    lines+=['','Before/at/after locates the English-to-partner transition relative to the critical permission-changing instruction. All layouts have four turns; neutral reminders preserve the preceding instruction and permission scope.', '',
            'English screen passed: '+str(summary['qualified_for_evaluation'])+'. The screen requires 7/8 in both full-history and reference-record conditions. No evaluation run is planned.','',
            '## Matched full-history differences','',
            '| Baseline | Comparison | Losses | Gains |','|---|---|---:|---:|']
    for r in result['matched_greedy_comparisons']:
        lines.append(f"| {r['baseline']} | {r['condition']} | {len(r['losses'])}/{r['blocks']} | {len(r['gains'])}/{r['blocks']} |")
    lines+=['','Losses mean the baseline was correct and comparison wrong on the same situation/variant; gains mean the reverse. These are descriptive counts, not significance tests.','',
            '## Reference-record identity control','',
            'For each situation, reference-record prompts are identical across all nine layouts. Distinct greedy responses: '+', '.join(f"{r['scenario']}: {r['unique_greedy_raw_outputs']}" for r in result['oracle_identity_checks'])+'.','',
            'See the machine-readable summary for record fields, invalids, unauthorized attempts, guarded completion and sampled-repeat correctness changes. This synthetic setup does not isolate translation, script, model capability or speech effects.']
    return '\n'.join(lines)+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    result=analyze(args.directory)
    args.output_dir.mkdir(parents=True,exist_ok=False)
    (args.output_dir/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (args.output_dir/'RESULTS.md').write_text(render(result),encoding='utf-8')
    print(json.dumps({'calls':result['summary']['requests'],'english_gate':result['summary']['english_gate']}))


if __name__=='__main__':main()
