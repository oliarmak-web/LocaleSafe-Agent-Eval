"""Free/local GPU collection for the frozen handoff development study."""
import argparse
import hashlib
import json
import platform
import random
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from .evaluate import read_jsonl, sha256
from .handoff_study import PROFILES, jobs_for, messages_for, score, seed_for

MODELS = {
    "mistral-7b-v03": {"model": "mistralai/Mistral-7B-Instruct-v0.3", "revision": "c170c708c41dac9275d15a8fff4eca08d52bab71",
        "weights": {"model-00001-of-00003.safetensors": "ce6fb6f6f4d0183f4813cbf4ece24109da629a08d4210da46f77e1d8b0bd5c19",
                    "model-00002-of-00003.safetensors": "8c0e72f148366b6a3709e002a98706a33d31aec8515090c856c95b2044f92ae0",
                    "model-00003-of-00003.safetensors": "905dd405363e43d95779c1c1155a2dbfd36155914ae95dbd934e12e490cfb4ca"}},
    "phi4-mini": {"model": "microsoft/Phi-4-mini-instruct", "revision": "cfbefacb99257ffa30c83adab238a50856ac3083",
        "weights": {"model-00001-of-00002.safetensors": "bc703090b63eda16f639fa4de7ac54635c23105ab1da2f6ec4d3403151d38ee6",
                    "model-00002-of-00002.safetensors": "7ff79b9d2d31076bac2663393451f6530f4fc8ca49b09002116c92c373dba983"}},
    "qwen3-4b": {"model": "Qwen/Qwen3-4B", "revision": "1cfa9a7208912126459214e8b04321603b3df60c",
        "weights": {"model-00001-of-00003.safetensors": "328a91d3122359d5547f9d79521205bc0a46e1f79a792dfe650e99fc2d651223",
                    "model-00002-of-00003.safetensors": "6cd087b316306a68c562436b5492edbcf6e16c6dba3a1308279caa5a58e21ca5",
                    "model-00003-of-00003.safetensors": "e4bf436957184f4eeb86a80e9db394503f1f56446b2e6b7edeac5b81470f4ca1"}},
    "smollm3-3b": {"model": "HuggingFaceTB/SmolLM3-3B", "revision": "a07cc9a04f16550a088caea529712d1d335b0ac1",
        "weights": {"model-00001-of-00002.safetensors": "e5eed4113a925264c33e3cdf76cd9f547c06a207ef2270914a7274a2bf685ffd",
                    "model-00002-of-00002.safetensors": "6c3ad90646457295723e4da5ee8afac47006e20407b122df5174693dd8d68a43"}},
}
SOURCES = ("localesafe/collect_handoff.py", "localesafe/handoff_study.py", "localesafe/handoff_eval.py",
           "localesafe/evaluate.py", "experiments/build_handoff_study.py", "experiments/handoff-study/PROTOCOL.md", "experiments/handoff-study/MODEL_EXTENSION.md")


def ordered_jobs(cases, profiles, seed):
    jobs = jobs_for(cases, profiles)
    result = []
    for stage in ("summary", "actor", "monitor"):
        group = [j for j in jobs if j["stage"] == stage]
        random.Random(f"{seed}:{stage}").shuffle(group)
        result.extend(group)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=MODELS, required=True)
    parser.add_argument("--cases", type=Path, default=Path("experiments/handoff-study/cases.jsonl"))
    parser.add_argument("--design", type=Path, default=Path("experiments/handoff-study/design.json"))
    parser.add_argument("--split", choices=("development", "evaluation"), required=True)
    parser.add_argument("--profiles", nargs="+", choices=PROFILES, default=list(PROFILES))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20261022)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--batch-size", type=int, choices=(1, 2, 4, 8), default=8)
    args = parser.parse_args()
    import torch
    import transformers
    from huggingface_hub import snapshot_download
    from transformers import AutoModelForCausalLM, AutoTokenizer, LogitsProcessor, LogitsProcessorList
    from transformers import TemperatureLogitsWarper, TopKLogitsWarper, TopPLogitsWarper
    if not torch.cuda.is_available():
        raise ValueError("CUDA required; no silent CPU/runtime substitution")
    torch.set_num_threads(2)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    cases = [c for c in read_jsonl(args.cases) if design[c["id"]]["split"] == args.split]
    if not cases:
        raise ValueError("empty split")
    indexed = {c["id"]: c for c in cases}
    jobs = ordered_jobs(cases, args.profiles, args.seed)
    spec = MODELS[args.model]
    settings = {"model": spec, "split": args.split, "profiles": args.profiles, "seed": args.seed,
                "all_cases_sha256": sha256(args.cases), "design_sha256": sha256(args.design),
                "sources": {name: sha256(name) for name in SOURCES}, "python": platform.python_version(),
                "torch": torch.__version__, "transformers": transformers.__version__, "cuda": torch.version.cuda,
                "gpu": torch.cuda.get_device_name(0), "dtype": "float16", "quantization": "none",
                "batch_size": args.batch_size, "threads": 2, "enable_thinking": False, "temperature": 0.7, "top_p": 0.8, "top_k": 20,
                "token_limits": {"summary": 192, "actor": 96, "monitor": 24},
                "sampling": "greedy or independent per-row CUDA seeded sampling with forced selected token"}
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=args.resume)
    manifest_path, log = output / "manifest.json", output / "attempts.jsonl"
    previous = {}
    if args.resume:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest["settings"] != settings or manifest["status"] != "started":
            raise ValueError("resume settings/status mismatch")
        saved = read_jsonl(log) if log.exists() and log.stat().st_size else []
        for row, job in zip(saved, jobs):
            case = indexed[job["case_id"]]
            if (row["job"] != job or row["messages"] != messages_for(case, job, previous)
                    or row["scores"] != score(case, job, row["raw_output"]) or row["seed"] != seed_for(case, job, args.seed)):
                raise ValueError("saved attempt mismatch")
            previous[job["id"]] = row
        if len(saved) > len(jobs):
            raise ValueError("unexpected extra attempts")
        manifest.setdefault("resumes", []).append({"preserved": len(saved), "prefix_sha256": sha256(log) if saved else None})
    else:
        manifest = {"status": "started", "started_utc": datetime.now(timezone.utc).isoformat(), "settings": settings,
                    "scheduled_requests": len(jobs)}
        (output / "cases.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False)+"\n" for c in cases), encoding="utf-8")
        shutil.copyfile(args.design, output / "design.json")
        for source in SOURCES:
            target = output / "source" / source
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    manifest_path.write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8")
    model_dir = Path(snapshot_download(spec["model"], revision=spec["revision"], token=False,
                                      allow_patterns=["*.json", "*.txt", "*.jinja", "*.model", "*.model.v3", "*.safetensors"],
                                      ignore_patterns=["consolidated.safetensors"]))
    for name, digest in spec["weights"].items():
        if sha256(model_dir / name) != digest:
            raise ValueError("model weight hash mismatch")
    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=False, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=False, local_files_only=True,
                                               use_safetensors=True, dtype=torch.float16, device_map="cuda").eval()
    tokenizer.padding_side = "left"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    class PerRowSampling(LogitsProcessor):
        def __init__(self, batch, seeds):
            self.batch = batch
            self.generators = [torch.Generator(device="cuda").manual_seed(s) for s in seeds]
            self.warpers = (TemperatureLogitsWarper(0.7), TopKLogitsWarper(20), TopPLogitsWarper(0.8))

        def __call__(self, input_ids, scores):
            warped = scores
            for warper in self.warpers:
                warped = warper(input_ids, warped)
            tokens = torch.stack([scores[i].argmax() if job["profile"] == "greedy" else
                                  torch.multinomial(torch.softmax(warped[i], dim=-1), 1,
                                                    generator=self.generators[i]).squeeze(0)
                                  for i, job in enumerate(self.batch)])
            forced = torch.full_like(scores, -float("inf"))
            forced[torch.arange(len(tokens), device="cuda"), tokens] = 0
            return forced

    with log.open("a" if args.resume else "x", encoding="utf-8") as stream:
        for stage in ("summary", "actor", "monitor"):
            stage_jobs = [j for j in jobs if j["stage"] == stage]
            for offset in range(0, len(stage_jobs), args.batch_size):
                batch = stage_jobs[offset:offset+args.batch_size]
                existing = [j["id"] in previous for j in batch]
                if all(existing):
                    continue
                if any(existing):
                    raise ValueError("partial saved batch")
                messages = [messages_for(indexed[j["case_id"]], j, previous) for j in batch]
                rendered = [tokenizer.apply_chat_template(m, tokenize=False, add_generation_prompt=True, enable_thinking=False) for m in messages]
                inputs = tokenizer(rendered, padding=True, return_tensors="pt").to("cuda")
                seeds = [seed_for(indexed[j["case_id"]], j, args.seed) for j in batch]
                start = time.perf_counter()
                with torch.inference_mode():
                    generated = model.generate(**inputs, max_new_tokens=settings["token_limits"][stage], do_sample=False,
                        logits_processor=LogitsProcessorList([PerRowSampling(batch, seeds)]), pad_token_id=tokenizer.pad_token_id)
                torch.cuda.synchronize()
                latency = round(time.perf_counter()-start, 4)
                lines = []
                for i, job in enumerate(batch):
                    tokens = generated[i, inputs.input_ids.shape[-1]:].tolist()
                    eos_ids = model.generation_config.eos_token_id
                    eos_ids = {eos_ids} if isinstance(eos_ids, int) else set(eos_ids or [])
                    end = next((k+1 for k, token in enumerate(tokens) if token in eos_ids), len(tokens))
                    tokens = tokens[:end]
                    raw = tokenizer.decode(tokens, skip_special_tokens=True).strip()
                    row = {"job": job, "seed": seeds[i], "messages": messages[i],
                           "prompt_sha256": hashlib.sha256(rendered[i].encode()).hexdigest(),
                           "raw_output": raw, "output_tokens": len(tokens), "batch_latency_seconds": latency,
                           "scores": score(indexed[job["case_id"]], job, raw)}
                    previous[job["id"]] = row
                    lines.append(json.dumps(row, ensure_ascii=False)+"\n")
                stream.write("".join(lines))
                stream.flush()
                print(f"{args.model} {args.split} {len(previous)}/{len(jobs)} {stage} batch={latency}s", flush=True)
    manifest.update(status="completed", completed_utc=datetime.now(timezone.utc).isoformat(),
                    attempts=len(previous), attempts_sha256=sha256(log), cases_sha256=sha256(output / "cases.jsonl"))
    manifest_path.write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8")
    hashes = {str(p.relative_to(output)).replace('\\', '/'): sha256(p) for p in output.rglob('*') if p.is_file()}
    (output / "archive-sha256.json").write_text(json.dumps(hashes, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
