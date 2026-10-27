"""Freeze all six choice orders for the existing draft language-pair cases."""
import json
from pathlib import Path
from experiments.build_hindi_pair import build
from localesafe.operation_probe import jobs_for


def main():
    cases,_=build()
    root=Path('experiments/operation-probe');root.mkdir(exist_ok=True)
    for name,value in [('cases.json',cases),('jobs.json',jobs_for(cases))]:
        with (root/name).open('x',encoding='utf-8',newline='\n') as stream:
            json.dump(value,stream,ensure_ascii=False,indent=2);stream.write('\n')
    print('336 planned calls; 56 rows; all six option permutations')


if __name__=='__main__':main()
