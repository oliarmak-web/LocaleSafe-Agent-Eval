"""Audit the post-hoc monitor intervention and retain paired changes."""
import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

from localesafe.collect_monitor_followup import score
from localesafe.evaluate import read_jsonl, sha256


def audit(directory):
    manifest=json.loads((directory/'manifest.json').read_text(encoding='utf-8'))
    if manifest['status']!='completed': raise ValueError('incomplete follow-up')
    hashes=json.loads((directory/'archive-sha256.json').read_text(encoding='utf-8'))
    for name,digest in hashes.items():
        path=(directory/name).resolve()
        if not path.is_relative_to(directory.resolve()) or sha256(path)!=digest: raise ValueError('archive hash mismatch')
    settings=manifest['settings']
    if sha256(directory/'jobs.json')!=settings['jobs_sha256'] or sha256(directory/'attempts.jsonl')!=manifest['attempts_sha256']:
        raise ValueError('artifact hash mismatch')
    for name,digest in settings['sources'].items():
        if sha256(directory/'source'/name)!=digest: raise ValueError('source hash mismatch')
    plan=json.loads((directory/'jobs.json').read_text(encoding='utf-8'))
    jobs=list(plan['jobs']); random.Random(settings['schedule_seed']).shuffle(jobs)
    rows=read_jsonl(directory/'attempts.jsonl')
    if len(rows)!=len(jobs) or len(rows)!=manifest['attempts'] or len(rows)!=manifest['scheduled_requests']:
        raise ValueError('incomplete grid')
    for row,job in zip(rows,jobs):
        if row['job_id']!=job['id'] or row['messages']!=job['messages'] or row['scores']!=score(job,row['raw_output']):
            raise ValueError('job/prompt/score mismatch')
        if type(row['output_tokens']) is not int or not 0<row['output_tokens']<=settings['max_new_tokens']:
            raise ValueError('invalid output token count')
    return manifest,plan,rows


def summarize(manifest,plan,rows):
    jobs={j['id']:j for j in plan['jobs']}
    groups=defaultdict(list); pairs=defaultdict(dict)
    for row in rows:
        job=jobs[row['job_id']]
        groups[job['parent'],job['condition']].append((job,row))
        pairs[job['parent'],job['parent_job_id']][job['condition']]=row
    results=[]
    for (parent,condition),group in sorted(groups.items()):
        counts={field:sum(r['scores'][field] for _,r in group) for field in ('parsed','correct','false_allow','false_block','abstained')}
        counts.update(parent=parent,condition=condition,requests=len(group),
                      permitted=sum(j['reference_allowed'] for j,_ in group),
                      forbidden=sum(not j['reference_allowed'] for j,_ in group))
        results.append(counts)
    contrasts=[]
    for parent in sorted({j['parent'] for j in jobs.values()}):
        for condition in ('explicit_rules','oracle_record'):
            counts={'parent':parent,'condition':condition,'pairs':0,'helped':0,'hurt':0,'both_correct':0,'both_wrong':0}
            for (source,_),group in pairs.items():
                if source!=parent: continue
                left,right=group['baseline_repeat']['scores']['correct'],group[condition]['scores']['correct']
                counts['pairs']+=1
                counts['both_correct' if left and right else 'hurt' if left else 'helped' if right else 'both_wrong']+=1
            contrasts.append(counts)
    return {'origin':'exploratory post-hoc monitor intervention','requests':len(rows),
            'attempts_sha256':manifest['attempts_sha256'],'conditions':results,'paired_changes':contrasts}


def render(summary):
    lines=['# Monitor intervention: fewer unsafe allows, more false blocks', '',
           '**384 new greedy Qwen3-4B calls. Exploratory follow-up designed after inspecting the initial results.**', '',
           'The same 128 fixed probes are judged under three conditions. The generated summaries and proposed actions stay fixed. Baseline-repeat prompts match the original run; explicit rules add a permission-check paragraph; oracle records replace generated records with the authored correct record.', '',
           '| Source families | Condition | Correct / all | False allows / forbidden | False blocks / permitted | Abstentions |',
           '|---|---|---:|---:|---:|---:|']
    for r in summary['conditions']:
        parent='development' if r['parent'].endswith('development') else 'evaluation'
        lines.append(f"| {parent} | {r['condition']} | {r['correct']}/{r['requests']} | {r['false_allow']}/{r['forbidden']} | {r['false_block']}/{r['permitted']} | {r['abstained']} |")
    lines += ['', '## Interpretation', '',
              'The explicit-rule prompt reduced false acceptance but blocked many permitted actions, lowering overall correctness. It was not a successful balanced fix in these cases. The oracle-record condition classified all 128 probes correctly, showing that this monitor can perform the bounded task with the reference representation.', '',
              'In the initial runs, Qwen preserved all permission fields but often represented requested_action as a string rather than the required tool-call object. A full reference record changes both the action representation and its contents; this follow-up does not isolate which field or wording explains the improvement.', '',
              'The baseline repeat reproduced the original greedy verdicts on every probe. Both source splits had already been inspected before this intervention was designed; neither is held out for this analysis. These are monitor judgments, not prevented production harm. Draft translations, small template counts and a single model limit generalization.', '',
              'The universal permission guard remains unchanged. A false allow by this model cannot authorize a real write in the sandbox.', '',
              '[Protocol](../experiments/monitor-followup/PROTOCOL.md) · [Raw archive](../experiments/results/monitor-followup-qwen3-4b-20261022/)']
    return '\n'.join(lines)+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    result=summarize(*audit(args.directory))
    args.output_dir.mkdir(parents=True,exist_ok=False)
    (args.output_dir/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (args.output_dir/'RESULTS.md').write_text(render(result),encoding='utf-8')
    print(json.dumps(result['conditions']))


if __name__=='__main__':
    main()
