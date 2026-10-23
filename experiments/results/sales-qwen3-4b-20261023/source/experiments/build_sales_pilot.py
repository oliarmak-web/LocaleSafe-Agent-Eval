"""Materialize the explicitly unreviewed sales-discovery pilot."""
import argparse
import json
from pathlib import Path

from localesafe.sales_pilot import cases


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args()
    a.output_dir.mkdir(parents=True,exist_ok=False)
    data=cases()
    (a.output_dir/'cases.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in data),encoding='utf-8')
    (a.output_dir/'design.json').write_text(json.dumps({c['id']:{'split':'development','family':c['family'],
                     'language':c['language'],'review_status':c['review_status']} for c in data},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'cases':len(data),'reviewed':0,'families':6,'languages':5}))


if __name__=='__main__':
    main()
