"""Collect the frozen exploratory output-contract prompt control on a free GPU."""
import argparse
import hashlib
import json
import platform
import random
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from .collect_handoff import MODELS
from .evaluate import sha256
from .handoff_study import score

SOURCES = ('localesafe/collect_format_followup.py', 'localesafe/collect_handoff.py',
           'localesafe/handoff_study.py', 'localesafe/handoff_eval.py', 'localesafe/evaluate.py',
           'experiments/build_format_followup.py', 'experiments/format-followup/PROTOCOL.md')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model', choices=('mistral-7b-v03', 'phi4-mini'), required=True)
    p.add_argument('--jobs', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    a = p.parse_args()
    import torch
    import transformers
    import accelerate
    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer, AutoModelForCausalLM
    if not torch.cuda.is_available():
        raise ValueError('CUDA required; no silent fallback')
    torch.set_num_threads(2)
    spec = MODELS[a.model]
    plan = json.loads(a.jobs.read_text(encoding='utf-8'))
    jobs = [j for j in plan['jobs'] if j['model'] == spec]
    if len(jobs) != 128 or len({j['id'] for j in jobs}) != 128:
        raise ValueError('expected exactly 128 unique jobs')
    random.Random(20261024).shuffle(jobs)
    batch_size = 1 if a.model == 'mistral-7b-v03' else 8
    out = a.output_dir
    out.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(a.jobs, out/'jobs.json')
    for source in SOURCES:
        target = out/'source'/source
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    settings = {'model': spec, 'jobs_sha256': sha256(a.jobs), 'sources': {s: sha256(s) for s in SOURCES},
                'python': platform.python_version(), 'torch': torch.__version__, 'transformers': transformers.__version__,
                'accelerate': accelerate.__version__, 'cuda': torch.version.cuda, 'gpu': torch.cuda.get_device_name(0),
                'dtype': 'float16', 'quantization': 'none', 'batch_size': batch_size, 'threads': 2,
                'decoding': 'greedy', 'max_new_tokens': 96, 'enable_thinking': False, 'schedule_seed': 20261024}
    manifest = {'status': 'started', 'started_utc': datetime.now(timezone.utc).isoformat(),
                'settings': settings, 'scheduled_requests': len(jobs)}
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    path = Path(snapshot_download(spec['model'], revision=spec['revision'], token=False,
                allow_patterns=['*.json','*.txt','*.jinja','*.model','*.model.v3','*.safetensors'],
                ignore_patterns=['consolidated.safetensors']))
    for name, digest in spec['weights'].items():
        if sha256(path/name) != digest:
            raise ValueError('weight hash mismatch')
    tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=False, local_files_only=True)
    tokenizer.padding_side = 'left'
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(path, trust_remote_code=False, local_files_only=True,
                 use_safetensors=True, dtype=torch.float16, device_map='cuda').eval()
    with (out/'attempts.jsonl').open('x', encoding='utf-8') as stream:
        for offset in range(0, len(jobs), batch_size):
            batch = jobs[offset:offset+batch_size]
            rendered = [tokenizer.apply_chat_template(j['messages'], tokenize=False, add_generation_prompt=True,
                        enable_thinking=False) for j in batch]
            inputs = tokenizer(rendered, padding=True, return_tensors='pt').to('cuda')
            start = time.perf_counter()
            with torch.inference_mode():
                generated = model.generate(**inputs, max_new_tokens=96, do_sample=False, pad_token_id=tokenizer.pad_token_id)
            torch.cuda.synchronize()
            latency = round(time.perf_counter()-start, 4)
            eos = model.generation_config.eos_token_id
            eos = {eos} if isinstance(eos, int) else set(eos or [])
            for i, job in enumerate(batch):
                tokens = generated[i, inputs.input_ids.shape[-1]:].tolist()
                end = next((k+1 for k, token in enumerate(tokens) if token in eos), len(tokens))
                tokens = tokens[:end]
                raw = tokenizer.decode(tokens, skip_special_tokens=True).strip()
                row = {'job_id': job['id'], 'messages': job['messages'], 'raw_output': raw,
                       'scores': score(job['case'], job['parent_job'], raw), 'output_tokens': len(tokens),
                       'prompt_sha256': hashlib.sha256(rendered[i].encode()).hexdigest(), 'batch_latency_seconds': latency}
                stream.write(json.dumps(row, ensure_ascii=False)+'\n')
            stream.flush()
            print(f"format follow-up {a.model} {min(offset+batch_size,len(jobs))}/{len(jobs)}", flush=True)
    manifest.update(status='completed', completed_utc=datetime.now(timezone.utc).isoformat(),
                    attempts=len(jobs), attempts_sha256=sha256(out/'attempts.jsonl'))
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    hashes = {p.relative_to(out).as_posix(): sha256(p) for p in out.rglob('*') if p.is_file()}
    (out/'archive-sha256.json').write_text(json.dumps(hashes, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
