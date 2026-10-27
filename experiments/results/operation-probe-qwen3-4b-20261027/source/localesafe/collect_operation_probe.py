"""Collect the frozen operation-choice probe on a free T4."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import random
import shutil
import time

from .collect_handoff import MODELS
from .evaluate import sha256
from .operation_probe import messages_for,score

SOURCES=('localesafe/collect_operation_probe.py','localesafe/operation_probe.py',
         'localesafe/collect_handoff.py','localesafe/handoff_study.py','localesafe/handoff_eval.py',
         'localesafe/evaluate.py','experiments/build_handoff_study.py','experiments/build_hindi_pair.py',
         'experiments/build_operation_probe.py','experiments/operation-probe/PROTOCOL.md')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args()
    import torch
    import transformers
    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer,AutoModelForCausalLM
    if not torch.cuda.is_available() or 'T4' not in torch.cuda.get_device_name(0):
        raise ValueError('Frozen protocol requires T4; no runtime substitution')
    torch.set_num_threads(2)
    spec=MODELS['qwen3-4b']
    cases=json.loads(Path('experiments/operation-probe/cases.json').read_text(encoding='utf-8'))
    jobs=json.loads(Path('experiments/operation-probe/jobs.json').read_text(encoding='utf-8'))
    if len(jobs)!=336 or len({j['id'] for j in jobs})!=336:raise ValueError('Invalid frozen job grid')
    indexed={c['id']:c for c in cases}
    random.Random(20261027).shuffle(jobs)
    out=a.output_dir;out.mkdir(parents=True,exist_ok=False)
    for name in ('cases.json','jobs.json'):shutil.copyfile(Path('experiments/operation-probe')/name,out/name)
    for name in SOURCES:
        target=out/'source'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(name,target)
    settings={'model':spec,'sources':{s:sha256(s) for s in SOURCES},'python':platform.python_version(),
              'torch':torch.__version__,'transformers':transformers.__version__,'cuda':torch.version.cuda,
              'gpu':torch.cuda.get_device_name(0),'dtype':'float16','quantization':'none','batch_size':8,
              'threads':2,'decoding':'greedy','enable_thinking':False,'max_new_tokens':8,'schedule_seed':20261027,
              'cases_sha256':sha256(out/'cases.json'),'jobs_sha256':sha256(out/'jobs.json')}
    manifest={'status':'started','started_utc':datetime.now(timezone.utc).isoformat(),'settings':settings,'scheduled_requests':336}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    model_path=Path(snapshot_download(spec['model'],revision=spec['revision'],token=False,
                    allow_patterns=['*.json','*.txt','*.jinja','*.model','*.model.v3','*.safetensors'],ignore_patterns=['consolidated.safetensors']))
    for name,digest in spec['weights'].items():
        if sha256(model_path/name)!=digest:raise ValueError('Weight hash mismatch')
    tokenizer=AutoTokenizer.from_pretrained(model_path,trust_remote_code=False,local_files_only=True)
    tokenizer.padding_side='left'
    if tokenizer.pad_token_id is None:tokenizer.pad_token=tokenizer.eos_token
    model=AutoModelForCausalLM.from_pretrained(model_path,trust_remote_code=False,local_files_only=True,
                    use_safetensors=True,dtype=torch.float16,device_map='cuda').eval()
    with (out/'attempts.jsonl').open('x',encoding='utf-8') as stream:
        for offset in range(0,len(jobs),8):
            batch=jobs[offset:offset+8]
            messages=[messages_for(indexed[j['case_id']],j) for j in batch]
            prompts=[tokenizer.apply_chat_template(m,tokenize=False,add_generation_prompt=True,enable_thinking=False) for m in messages]
            inputs=tokenizer(prompts,padding=True,return_tensors='pt').to('cuda')
            start=time.perf_counter()
            with torch.inference_mode():
                output=model.generate(**inputs,max_new_tokens=8,do_sample=False,pad_token_id=tokenizer.pad_token_id)
            torch.cuda.synchronize();latency=round(time.perf_counter()-start,4)
            eos=model.generation_config.eos_token_id;eos={eos} if isinstance(eos,int) else set(eos or [])
            for i,j in enumerate(batch):
                tokens=output[i,inputs.input_ids.shape[-1]:].tolist()
                end=next((k+1 for k,t in enumerate(tokens) if t in eos),len(tokens));tokens=tokens[:end]
                raw=tokenizer.decode(tokens,skip_special_tokens=True).strip()
                row={'job':j,'messages':messages[i],'prompt_sha256':hashlib.sha256(prompts[i].encode()).hexdigest(),
                     'raw_output':raw,'output_tokens':len(tokens),'batch_latency_seconds':latency,
                     'scores':score(indexed[j['case_id']],j,raw)}
                stream.write(json.dumps(row,ensure_ascii=False)+'\n')
            stream.flush();print(f'operation probe {min(offset+8,336)}/336',flush=True)
    manifest.update(status='completed',attempts=336,completed_utc=datetime.now(timezone.utc).isoformat(),attempts_sha256=sha256(out/'attempts.jsonl'))
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    hashes={p.relative_to(out).as_posix():sha256(p) for p in out.rglob('*') if p.is_file()}
    (out/'archive-sha256.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
