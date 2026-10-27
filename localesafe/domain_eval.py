"""Export domain checkpoints or score local agent replies without API keys."""
import argparse
import json
from pathlib import Path
from .domain_study import cases,LANGUAGES,messages_for,expected_action,score


def evaluate(data,traces,origin):
    if origin not in ('model','synthetic'):raise ValueError('Declare model or synthetic trace origin')
    indexed={c['id']:c for c in data};outputs={}
    for row in traces:
        if (not isinstance(row,dict) or set(row)!={'case_id','raw_output'} or not isinstance(row['case_id'],str)
            or row['case_id'] not in indexed or row['case_id'] in outputs or not isinstance(row['raw_output'],str)):
            raise ValueError('Unknown/duplicate case or invalid trace fields')
        outputs[row['case_id']]=row['raw_output']
    rows=[{'case_id':c['id'],'domain':c['domain'],'language':c['language'],
           'missing':c['id'] not in outputs,'scores':score(c,{'stage':'qualify_history'},outputs.get(c['id'],''))} for c in data]
    return {'trace_origin':origin,'cases':len(data),'provided':len(outputs),'missing':len(data)-len(outputs),
            'counts':{key:sum(r['scores'][key] for r in rows) for key in ('parsed','correct','operation_correct','unauthorized_attempt','guard_blocked','executed')},
            'rows':rows,'notice':'Local checkpoint scoring and guarded mock state only. Trace origin is caller-declared; no model or external service was invoked.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);group=p.add_mutually_exclusive_group(required=True)
    group.add_argument('--reference-demo',action='store_true');group.add_argument('--traces',type=Path);group.add_argument('--export-prompts',action='store_true')
    p.add_argument('--language',choices=LANGUAGES);p.add_argument('--trace-origin',choices=('model','synthetic'));p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();data=[c for c in cases() if not a.language or c['language']==a.language]
    if a.export_prompts:
        result=[{'case_id':c['id'],'messages':messages_for(c,{'stage':'qualify_history'},{})} for c in data]
    else:
        if a.reference_demo:
            traces=[{'case_id':c['id'],'raw_output':json.dumps(expected_action(c),ensure_ascii=False)} for c in data];origin='synthetic'
        else:
            if not a.trace_origin:p.error('--traces requires --trace-origin')
            traces=[json.loads(line) for line in a.traces.read_text(encoding='utf-8').splitlines() if line.strip()];origin=a.trace_origin
        result=evaluate(data,traces,origin)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('x',encoding='utf-8') as stream:
        if a.export_prompts:
            for row in result:stream.write(json.dumps(row,ensure_ascii=False)+'\n')
        else:json.dump(result,stream,ensure_ascii=False,indent=2);stream.write('\n')
    print(json.dumps({'exported_prompts':len(result)} if a.export_prompts else {k:result[k] for k in ('trace_origin','cases','provided','missing','counts')}))


if __name__=='__main__':main()
