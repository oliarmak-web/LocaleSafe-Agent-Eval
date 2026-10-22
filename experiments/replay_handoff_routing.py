"""Post-hoc cached-output routing replay, not new model calls or a deployment."""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from experiments.summarize_handoff import audit
from localesafe.handoff_contract import validate_record


def replay(directory):
    manifest,cases,rows=audit(directory)
    index={(r['job']['case_id'],r['job']['profile'],r['job']['stage'],r['job']['condition']):r for r in rows}
    groups=defaultdict(list)
    details=[]
    for case in cases:
        for profile in manifest['settings']['profiles']:
            raw=index[case['id'],profile,'summary','record']['raw_output']
            valid,reason=validate_record(raw,case['principal'],set(case['initial_state']),case['events'][-1]['version'],case['events'][-1]['event_id'])
            chosen=index[case['id'],profile,'actor','generated_record' if valid else 'full_history']
            baseline=index[case['id'],profile,'actor','generated_record']
            item={'case_id':case['id'],'profile':profile,'language_pattern':case['language_pattern'],
                  'contract_valid':valid,'reason':reason,'selected_job_id':chosen['job']['id'],
                  'correct':chosen['scores']['correct'],'baseline_correct':baseline['scores']['correct'],
                  'unauthorized_attempt':chosen['scores']['unauthorized_attempt']}
            groups[profile].append(item)
            details.append(item)
    return {'model':manifest['settings']['model']['model'],'split':manifest['settings']['split'],
            'new_model_calls':0,'origin':'post-hoc cached routing replay',
            'parent_attempts_sha256':manifest['attempts_sha256'],
            'profiles':{profile:{'cases':len(items),'fallbacks':sum(not i['contract_valid'] for i in items),
                       'correct':sum(i['correct'] for i in items),'baseline_correct':sum(i['baseline_correct'] for i in items),
                       'unauthorized_attempts':sum(i['unauthorized_attempt'] for i in items),
                       'reasons':dict(Counter(i['reason'] for i in items))} for profile,items in groups.items()},
            'rows':details}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directories',nargs='+',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=[replay(path) for path in args.directories]
    with args.output.open('x',encoding='utf-8') as stream:
        stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k!='rows'} for r in result]))


if __name__=='__main__':
    main()
