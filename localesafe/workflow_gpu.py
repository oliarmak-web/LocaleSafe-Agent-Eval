"""GPU replication of the frozen workflow tasks; no quantization or credentials."""
import argparse
import hashlib
import json
import platform
import random
import time
from datetime import datetime, timezone
from pathlib import Path

from .evaluate import read_jsonl, sha256
from .workflow_probe import MODEL_SPECS, jobs_for, messages_for, score, seed_for


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=MODEL_SPECS, required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--cases", default="experiments/workflow/cases.jsonl")
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20261024)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    import torch
    import transformers
    from huggingface_hub import snapshot_download
    from transformers import AutoModelForCausalLM, AutoTokenizer, LogitsProcessor, LogitsProcessorList
    from transformers import TemperatureLogitsWarper, TopKLogitsWarper, TopPLogitsWarper
    if not torch.cuda.is_available():
        raise ValueError("GPU unavailable; do not silently change runtime")
    if args.repeats < 1:
        parser.error("positive repeats required")
    torch.set_num_threads(2)
    spec = MODEL_SPECS[args.model]
    model_dir = Path(snapshot_download(spec["model"], revision=spec["revision"], token=False,
                                      allow_patterns=["*.json", "*.txt", "*.jinja", "*.safetensors"]))
    for name, digest in spec["weights"].items():
        if sha256(model_dir / name) != digest:
            raise ValueError("weight hash mismatch")
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=args.resume)
    settings = {"model": spec, "cases_sha256": sha256(args.cases), "collector_sha256": sha256(__file__),
                "builder_sha256": sha256("experiments/build_workflow_cases.py"), "shared_scorer_sha256": sha256("localesafe/workflow_probe.py"),
                "python": platform.python_version(), "torch": torch.__version__, "transformers": transformers.__version__,
                "repeats": args.repeats, "seed": args.seed, "temperature": 0.7, "top_p": 0.8, "top_k": 20,
                "max_new_tokens": 64, "enable_thinking": False, "dtype": "float16", "device": "cuda", "threads": 2,
                "batch_size": 8, "sampling": "per-row CUDA seeded generator; temperature/top-k/top-p warpers; forced sampled token",
                "quantization": "none", "gpu": torch.cuda.get_device_name(0), "cuda": torch.version.cuda}
    records = read_jsonl(args.cases)
    indexed = {r["id"]: r for r in records}
    jobs = jobs_for(records, args.repeats)
    random.Random(args.seed).shuffle(jobs)
    path = output / "manifest.json"
    log = output / "attempts.jsonl"
    manifest = {"status": "started", "started_utc": datetime.now(timezone.utc).isoformat(), "settings": settings}
    done = set()
    if args.resume:
        manifest = json.loads(path.read_text())
        if manifest["status"] != "started" or manifest["settings"] != settings or sha256(output / "cases.jsonl") != settings["cases_sha256"]:
            raise ValueError("resume settings mismatch")
        saved = read_jsonl(log) if log.exists() and log.stat().st_size else []
        for row in saved:
            key = row["id"], row["condition"], row["repeat"]
            record = indexed[row["id"]]
            if key in done or key not in jobs or row["scores"] != score(record, row["condition"], row["raw_output"]) or row["messages"] != messages_for(record, row["condition"]) or row["seed"] != seed_for(record["scenario"], row["condition"], row["repeat"], args.seed):
                raise ValueError("saved attempt mismatch")
            done.add(key)
        manifest.setdefault("resumes", []).append({"preserved": len(saved), "prefix_sha256": sha256(log) if saved else None,
                                                   "utc": datetime.now(timezone.utc).isoformat()})
    else:
        (output / "cases.jsonl").write_bytes(Path(args.cases).read_bytes())
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=False, local_files_only=True, padding_side="left")
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=False, local_files_only=True,
                                               use_safetensors=True, dtype=torch.float16).to("cuda").eval()

    class IndependentSampling(LogitsProcessor):
        def __init__(self, seeds):
            self.generators = [torch.Generator(device="cuda").manual_seed(seed) for seed in seeds]
            self.warpers = [TemperatureLogitsWarper(0.7), TopKLogitsWarper(20), TopPLogitsWarper(0.8)]

        def __call__(self, input_ids, scores):
            for warper in self.warpers:
                scores = warper(input_ids, scores)
            selected = [torch.multinomial(torch.softmax(scores[i], dim=-1), 1, generator=g).item() for i, g in enumerate(self.generators)]
            forced = torch.full_like(scores, -float("inf"))
            for i, token in enumerate(selected):
                forced[i, token] = 0
            return forced

    with log.open("a" if args.resume else "x", encoding="utf-8") as stream:
        for start_index in range(0, len(jobs), settings["batch_size"]):
            batch = jobs[start_index:start_index + settings["batch_size"]]
            if all(job in done for job in batch):
                continue
            if any(job in done for job in batch):
                raise ValueError("partial saved batch; preserve and investigate")
            seeds = [seed_for(indexed[ident]["scenario"], condition, repeat, args.seed) for ident, condition, repeat in batch]
            messages_batch = [messages_for(indexed[ident], condition) for ident, condition, repeat in batch]
            rendered = [tokenizer.apply_chat_template(m, tokenize=False, add_generation_prompt=True, enable_thinking=False) for m in messages_batch]
            inputs = tokenizer(rendered, return_tensors="pt", padding=True).to("cuda")
            start = time.perf_counter()
            with torch.inference_mode():
                generated = model.generate(**inputs, max_new_tokens=64, do_sample=False,
                                           logits_processor=LogitsProcessorList([IndependentSampling(seeds)]), pad_token_id=tokenizer.pad_token_id)
            torch.cuda.synchronize()
            latency = round(time.perf_counter() - start, 4)
            lines = []
            for i, (ident, condition, repeat) in enumerate(batch):
                record = indexed[ident]
                tokens = generated[i][inputs.input_ids.shape[-1]:].tolist()
                end_ids = model.generation_config.eos_token_id
                end_ids = [end_ids] if isinstance(end_ids, int) else end_ids
                for j, token in enumerate(tokens):
                    if token in end_ids:
                        tokens = tokens[:j + 1]
                        break
                raw = tokenizer.decode(tokens, skip_special_tokens=True).strip()
                row = {"id": ident, "scenario": record["scenario"], "language": record["language"], "family": record["family"],
                       "condition": condition, "repeat": repeat, "seed": seeds[i], "messages": messages_batch[i],
                       "prompt_sha256": hashlib.sha256(rendered[i].encode()).hexdigest(), "raw_output": raw,
                       "output_tokens": len(tokens), "batch_index": start_index // settings["batch_size"], "batch_latency_seconds": latency,
                       "scores": score(record, condition, raw)}
                lines.append(json.dumps(row, ensure_ascii=False) + "\n")
            stream.write("".join(lines))
            stream.flush()
            print(f"{args.model} {start_index + len(batch)}/{len(jobs)} recorded; batch {latency}s", flush=True)
    manifest.update(status="completed", completed_utc=datetime.now(timezone.utc).isoformat(), attempts_sha256=sha256(log), attempts=len(jobs))
    path.write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
