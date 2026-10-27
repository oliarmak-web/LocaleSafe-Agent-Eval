"""Local CPU Whisper smoke test; public files only, no inference API."""
import argparse
import copy
from datetime import datetime,timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import random
import shutil
import time

from .asr_metrics import score
from .evaluate import sha256

MODEL={'model':'openai/whisper-small','revision':'973afd24965f72e36ca33b3055d56a652f456b4d',
       'weights_sha256':'1d7734884874f1a1513ed9aa760a4f8e97aaa02fd6d93a3a85d27b2ae9ca596b'}
SOURCES=('localesafe/collect_audio_smoke.py','localesafe/asr_metrics.py','localesafe/evaluate.py',
         'experiments/fetch_public_audio.py','experiments/audio-pilot/PROTOCOL.md')


def jobs_for(samples):
    jobs=[{'id':s['id']+':'+arm,'sample_id':s['id'],'arm':arm,'language':s['language'] if arm=='provided_language' else None}
          for s in samples for arm in ('auto_language','provided_language')]
    random.Random(20261027).shuffle(jobs)
    return jobs


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--packet',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args()
    import io
    import numpy as np
    import scipy
    from scipy.signal import resample_poly
    import soundfile as sf
    import torch
    import transformers
    from huggingface_hub import snapshot_download
    from transformers import WhisperProcessor,WhisperForConditionalGeneration
    torch.set_num_threads(4);torch.set_num_interop_threads(1);torch.manual_seed(20261027);torch.use_deterministic_algorithms(True)
    packet=json.loads((a.packet/'samples.json').read_text(encoding='utf-8'));samples=packet['samples']
    if len(samples)!=20 or len({s['id'] for s in samples})!=20:raise ValueError('Expected frozen 20-clip packet')
    indexed={s['id']:s for s in samples};jobs=jobs_for(samples)
    out=a.output_dir;out.mkdir(parents=True,exist_ok=False)
    shutil.copyfile(a.packet/'samples.json',out/'samples.json')
    for name in SOURCES:
        target=out/'source'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(name,target)
    settings={'model':MODEL,'device':'cpu','dtype':'float32','threads':4,'interop_threads':1,'deterministic_algorithms':True,
              'python':platform.python_version(),'torch':torch.__version__,'transformers':transformers.__version__,
              'numpy':np.__version__,'scipy':scipy.__version__,'soundfile':sf.__version__,
              'sources':{s:sha256(s) for s in SOURCES},'samples_sha256':sha256(out/'samples.json'),
              'decoding':'greedy','beams':1,'task':'transcribe','timestamps':False,'max_new_tokens':128,'schedule_seed':20261027}
    manifest={'status':'started','started_utc':datetime.now(timezone.utc).isoformat(),'settings':settings,'scheduled_requests':40}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    path=Path(snapshot_download(MODEL['model'],revision=MODEL['revision'],token=False,
                               allow_patterns=['*.json','*.txt','model.safetensors'],local_dir='reports/whisper-small-pinned'))
    if sha256(path/'model.safetensors')!=MODEL['weights_sha256']:raise ValueError('Whisper weight hash mismatch')
    processor=WhisperProcessor.from_pretrained(path,local_files_only=True,trust_remote_code=False)
    model=WhisperForConditionalGeneration.from_pretrained(path,use_safetensors=True,local_files_only=True,
                              trust_remote_code=False,dtype=torch.float32,attn_implementation='eager').to('cpu').eval()
    (out/'generation-defaults.json').write_text(json.dumps(model.generation_config.to_dict(),indent=2)+'\n',encoding='utf-8')
    prepared={}
    with (out/'attempts.jsonl').open('x',encoding='utf-8') as stream:
        for n,job in enumerate(jobs,1):
            sample=indexed[job['sample_id']]
            if sample['id'] not in prepared:
                audio=(a.packet/sample['audio_file']).resolve()
                if not audio.is_relative_to(a.packet.resolve()) or sha256(audio)!=sample['audio_sha256']:raise ValueError('Audio path/hash mismatch')
                waveform,rate=sf.read(audio,dtype='float32',always_2d=True)
                waveform=waveform.mean(axis=1)
                divisor=math.gcd(rate,16000)
                if rate!=16000:waveform=resample_poly(waveform,16000//divisor,rate//divisor).astype(np.float32)
                waveform=np.ascontiguousarray(waveform,dtype=np.float32)
                features=processor(waveform,sampling_rate=16000,return_tensors='pt',return_attention_mask=True)
                prepared[sample['id']]=(features,hashlib.sha256(waveform.tobytes()).hexdigest())
            features,waveform_hash=prepared[sample['id']]
            cfg=copy.deepcopy(model.generation_config)
            cfg.language=job['language'];cfg.task='transcribe';cfg.forced_decoder_ids=None
            cfg.do_sample=False;cfg.num_beams=1;cfg.max_new_tokens=128;cfg.return_timestamps=False
            start=time.perf_counter()
            with torch.inference_mode():
                generated=model.generate(input_features=features.input_features,attention_mask=features.attention_mask,
                                         generation_config=cfg,return_dict_in_generate=True)
            sequence=generated.sequences[0].tolist()
            raw=processor.tokenizer.decode(sequence,skip_special_tokens=True)
            eos=cfg.eos_token_id;eos={eos} if isinstance(eos,int) else set(eos or [])
            row={'job':job,'raw_output':raw,'token_ids':sequence,'waveform_sha256':waveform_hash,
                 'input_features_sha256':hashlib.sha256(features.input_features.numpy().tobytes()).hexdigest(),
                 'latency_seconds':round(time.perf_counter()-start,4),
                 'no_eos_at_budget':not any(t in eos for t in sequence) and len(sequence)>=128,
                 'scores':score(sample['reference'],raw)}
            stream.write(json.dumps(row,ensure_ascii=False)+'\n');stream.flush()
            print(f'audio smoke {n}/40',flush=True)
    manifest.update(status='completed',attempts=40,attempts_sha256=sha256(out/'attempts.jsonl'),completed_utc=datetime.now(timezone.utc).isoformat())
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    hashes={p.relative_to(out).as_posix():sha256(p) for p in out.rglob('*') if p.is_file()}
    (out/'archive-sha256.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
