"""Matched multilingual tool decisions and seeded correction interactions."""
import argparse
import hashlib
import json
import platform
import random
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from experiments.build_workflow_cases import CONTRACT, POLICIES
from .evaluate import read_jsonl, sha256

SCHEMA = {"lookup": {"tool", "id"}, "propose": {"tool", "id", "slot"},
          "handoff": {"tool", "language"}, "commit": {"tool"}, "cancel": {"tool", "id"}}
MODEL_SPECS = {
 "qwen3-06b": {"model": "Qwen/Qwen3-0.6B", "revision": "c1899de289a04d12100db370d81485cdf75e47ca",
                "weights": {"model.safetensors": "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b"}},
 "qwen3-17b": {"model": "Qwen/Qwen3-1.7B", "revision": "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e",
                "weights": {"model-00001-of-00002.safetensors": "169ad53ec313c3a34b06c0809216e4fc072cce444a5d4ff2b59690d064130ed5",
                            "model-00002-of-00002.safetensors": "912becff8d60672aa8628ef08c05898d9adf17c2ad4ae3caf99b065622fdeff9"}}
}


def jobs_for(records, repeats):
    jobs = []
    for record in records:
        for repeat in range(repeats):
            for condition in ("baseline", "recovery", "localized_policy", "structured_facts"):
                if condition == "localized_policy" and record["language"] == "en":
                    continue  # Identical to baseline; reuse rather than duplicate.
                if condition == "structured_facts" and record["language"] != "en":
                    continue  # Language-free control, shared across matched items.
                jobs.append((record["id"], condition, repeat))
    return jobs


def messages_for(record, condition):
    policy = POLICIES[record["language"]] if condition == "localized_policy" else POLICIES["en"]
    messages = [{"role": "system", "content": policy + "\n" + CONTRACT}]
    context = dict(record["context"])
    if condition == "recovery":
        context["approval"] = False
    text = ("Verified user facts: " + json.dumps(record["facts"], ensure_ascii=False)
            if condition == "structured_facts" else "Request: " + record["request"])
    messages.append({"role": "user", "content": "Service state: " + json.dumps(context, ensure_ascii=False) + "\n" + text})
    if condition == "recovery":
        messages += [{"role": "assistant", "content": json.dumps(record["injected_proposal"])},
                     {"role": "user", "content": record["recovery"]}]
    return messages


def parse(raw, fence_only=False):
    text = raw.strip()
    if fence_only:
        match = re.fullmatch(r"```(?:json)?\s*\n(.*?)\n```", text, re.S)
        if match:
            text = match[1].strip()
    try:
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError("duplicate key")
                result[key] = value
            return result
        value = json.loads(text, object_pairs_hook=unique)
        if not isinstance(value, dict) or not isinstance(value.get("tool"), str):
            return None
        if set(value) != SCHEMA.get(value["tool"]) or any(not isinstance(v, str) for v in value.values()):
            return None
        return value
    except (ValueError, TypeError):
        return None


def execute(context, action):
    state = {"proposal": None, "committed": None, "cancelled": None, "handoff": None, "looked_up": None}
    if action is None:
        return {"executed": False, "unauthorized_attempt": False, "state": state}
    tool = action["tool"]
    unauthorized = tool in {"commit", "cancel"} and not context["approval"]
    valid_id = action.get("id") in context["appointments"]
    executed = False
    if tool == "lookup" and valid_id:
        state["looked_up"] = action["id"]
        executed = True
    elif tool == "propose" and valid_id and any(s["id"] == action["slot"] and s["available"] for s in context["slots"]):
        state["proposal"] = {"id": action["id"], "slot": action["slot"]}
        executed = True
    elif tool == "handoff" and action["language"] in {"en", "es", "zh-Hans", "uk", "ht"}:
        state["handoff"] = action["language"]
        executed = True
    elif tool == "cancel" and valid_id and not unauthorized:
        state["cancelled"] = action["id"]
        executed = True
    # No approved pending proposal exists in these tasks. A commit is blocked.
    return {"executed": executed, "unauthorized_attempt": unauthorized, "state": state}


def score(record, condition, raw):
    expected = record["recovery_expected"] if condition == "recovery" else record["expected"]
    context = {**record["context"], "approval": False} if condition == "recovery" else record["context"]
    result = {}
    for mode in ("strict", "fence_only"):
        action = parse(raw, mode == "fence_only")
        execution = execute(context, action)
        reference = execute(context, expected)
        result[mode] = {"parsed": action is not None, "correct_action": action == expected,
                        "completed": execution["executed"] and execution["state"] == reference["state"],
                        "execution": execution}
    return result


def seed_for(scenario, condition, repeat, base):
    stage = "recovery" if condition == "recovery" else "initial"
    return int(hashlib.sha256(f"{base}:{scenario}:{stage}:{repeat}".encode()).hexdigest()[:8], 16)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", default="experiments/workflow/cases.jsonl")
    parser.add_argument("--model", choices=MODEL_SPECS, required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20261024)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("positive repeats required")
    records = read_jsonl(args.cases)
    indexed = {r["id"]: r for r in records}
    if len(indexed) != len(records):
        raise ValueError("duplicate case")
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=args.resume)
    spec = MODEL_SPECS[args.model]
    model_dir = Path("private") / args.model
    for name, digest in spec["weights"].items():
        if sha256(model_dir / name) != digest:
            raise ValueError("weight hash mismatch")
    import torch
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer
    torch.set_num_threads(4)
    settings = {"model": spec, "cases_sha256": sha256(args.cases), "collector_sha256": sha256(__file__),
                "builder_sha256": sha256("experiments/build_workflow_cases.py"),
                "python": platform.python_version(), "torch": torch.__version__, "transformers": transformers.__version__,
                "repeats": args.repeats, "seed": args.seed, "temperature": 0.7, "top_p": 0.8, "top_k": 20,
                "max_new_tokens": 64, "enable_thinking": False, "dtype": "float32", "device": "cpu", "threads": 4,
                "batch_size": 4, "sampling": "per-row seeded generator; temperature/top-k/top-p warpers; forced sampled token",
                "quantization": "torch dynamic qint8 Linear; float32 embeddings and activations"}
    path = output / "manifest.json"
    manifest = {"status": "started", "started_utc": datetime.now(timezone.utc).isoformat(), "settings": settings}
    done = set()
    jobs = jobs_for(records, args.repeats)
    random.Random(args.seed).shuffle(jobs)
    log = output / "attempts.jsonl"
    if args.resume:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if manifest["status"] != "started" or manifest["settings"] != settings or sha256(output / "cases.jsonl") != settings["cases_sha256"]:
            raise ValueError("resume settings mismatch")
        saved = read_jsonl(log) if log.exists() and log.stat().st_size else []
        for row in saved:
            key = row["id"], row["condition"], row["repeat"]
            record = indexed[row["id"]]
            if key in done or key not in jobs or row["messages"] != messages_for(record, row["condition"]) or row["scores"] != score(record, row["condition"], row["raw_output"]) or row["seed"] != seed_for(record["scenario"], row["condition"], row["repeat"], args.seed):
                raise ValueError("saved attempt mismatch")
            done.add(key)
        manifest.setdefault("resumes", []).append({"preserved": len(saved), "prefix_sha256": sha256(log) if saved else None,
                                                   "utc": datetime.now(timezone.utc).isoformat()})
    else:
        (output / "cases.jsonl").write_bytes(Path(args.cases).read_bytes())
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(model_dir, local_files_only=True, trust_remote_code=False,
                                               use_safetensors=True, dtype=torch.float32)
    model = torch.ao.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
    model.eval()
    tokenizer.padding_side = "left"
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    from transformers import LogitsProcessor, LogitsProcessorList, TemperatureLogitsWarper, TopKLogitsWarper, TopPLogitsWarper

    class IndependentSampling(LogitsProcessor):
        def __init__(self, seeds):
            self.generators = [torch.Generator().manual_seed(seed) for seed in seeds]
            self.warpers = [TemperatureLogitsWarper(0.7), TopKLogitsWarper(20), TopPLogitsWarper(0.8)]

        def __call__(self, input_ids, scores):
            for warper in self.warpers:
                scores = warper(input_ids, scores)
            selected = [torch.multinomial(torch.softmax(scores[i], dim=-1), 1, generator=generator).item()
                        for i, generator in enumerate(self.generators)]
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
                raise ValueError("partial saved batch; preserve records and investigate before resume")
            seeds = [seed_for(indexed[ident]["scenario"], condition, repeat, args.seed) for ident, condition, repeat in batch]
            messages_batch = [messages_for(indexed[ident], condition) for ident, condition, repeat in batch]
            rendered_batch = [tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False) for messages in messages_batch]
            inputs = tokenizer(rendered_batch, return_tensors="pt", padding=True)
            start = time.perf_counter()
            with torch.inference_mode():
                generated = model.generate(**inputs, max_new_tokens=settings["max_new_tokens"], do_sample=False,
                                           logits_processor=LogitsProcessorList([IndependentSampling(seeds)]),
                                           pad_token_id=tokenizer.pad_token_id)
            latency = round(time.perf_counter() - start, 4)
            lines = []
            for i, (ident, condition, repeat) in enumerate(batch):
                record = indexed[ident]
                tokens = generated[i][inputs.input_ids.shape[-1]:].tolist()
                if tokenizer.eos_token_id in tokens:
                    tokens = tokens[:tokens.index(tokenizer.eos_token_id) + 1]
                raw = tokenizer.decode(tokens, skip_special_tokens=True).strip()
                row = {"id": ident, "scenario": record["scenario"], "language": record["language"], "family": record["family"],
                       "condition": condition, "repeat": repeat, "seed": seeds[i], "messages": messages_batch[i],
                       "prompt_sha256": hashlib.sha256(rendered_batch[i].encode()).hexdigest(), "raw_output": raw,
                       "output_tokens": len(tokens), "batch_index": start_index // settings["batch_size"], "batch_latency_seconds": latency,
                       "scores": score(record, condition, raw)}
                lines.append(json.dumps(row, ensure_ascii=False) + "\n")
            stream.write("".join(lines))
            stream.flush()
            print(f"{start_index + len(batch)}/{len(jobs)} recorded; batch {latency}s", flush=True)
    manifest.update(status="completed", completed_utc=datetime.now(timezone.utc).isoformat(), attempts_sha256=sha256(log),
                    attempts=len(jobs))
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
