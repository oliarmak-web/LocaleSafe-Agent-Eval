"""Freeze the cross-domain feasibility grid; all translations remain drafts."""
import json
from pathlib import Path
from localesafe.domain_study import cases


def main():
    root=Path('experiments/domain-study');root.mkdir(exist_ok=True)
    data=cases()
    design={c['id']:{'split':'development','domain':c['domain'],'family':c['family'],'language':c['language'],
                      'review_status':c['review_status']} for c in data}
    for name,text in [('cases.jsonl',''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in data)),
                      ('design.json',json.dumps(design,indent=2)+'\n')]:
        with (root/name).open('x',encoding='utf-8',newline='\n') as stream:stream.write(text)
    print('180 draft rows; five fictional policies; six shared intent families; 720 planned calls')


if __name__=='__main__':main()
