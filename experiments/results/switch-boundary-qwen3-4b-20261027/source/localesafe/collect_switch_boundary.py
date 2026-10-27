"""Frozen actor/record subset of the existing handoff collector."""
import sys
from . import collect_handoff as collector
from .handoff_study import jobs_for as full_jobs

EXTRA_SOURCES = ('localesafe/collect_switch_boundary.py','experiments/build_switch_boundary.py',
                 'experiments/build_hindi_pair.py','experiments/switch-boundary/PROTOCOL.md')


def jobs_for(cases, profiles):
    return [j for j in full_jobs(cases,profiles) if
            (j['stage']=='summary' and j['condition']=='record') or
            (j['stage']=='actor' and j['condition'] in ('full_history','oracle_record','generated_record'))]


def ordered_jobs(cases, profiles, seed):
    import random
    jobs=jobs_for(cases,profiles)
    result=[]
    for stage in ('summary','actor'):
        group=[j for j in jobs if j['stage']==stage]
        random.Random(f'{seed}:{stage}').shuffle(group)
        result.extend(group)
    return result


def main():
    if '--cases' in sys.argv or '--design' in sys.argv:
        raise ValueError('Use frozen boundary cases/design')
    if '--model' not in sys.argv or sys.argv[sys.argv.index('--model')+1]!='qwen3-4b':
        raise ValueError('Frozen run uses qwen3-4b')
    collector.SOURCES=(*collector.SOURCES,*EXTRA_SOURCES)
    collector.ordered_jobs=ordered_jobs
    sys.argv += ['--cases','experiments/switch-boundary/cases.jsonl','--design','experiments/switch-boundary/design.json']
    collector.main()


if __name__=='__main__':main()
