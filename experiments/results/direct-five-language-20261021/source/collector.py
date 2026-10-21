"""Free-form date interpretation: no offered answers or A/B/C labels."""

import argparse
import hashlib
import json
import platform
import random
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from experiments.build_attribution_cases import compile_date
from .evaluate import read_jsonl, sha256
from .service_eval import date_context, replay, validate_cases

POLICY = """Interpret a requested appointment date in a fictional service.
Use explicitly supplied locale, never the request's language. US numeric dates use month/day/year; GB uses day/month/year.
If a numeric date has two possible interpretations and no locale is supplied, request clarification.
Explicit ISO dates and explicit month names do not require a numeric-date convention.
Return only the interpreted ISO date YYYY-MM-DD, or the single word CLARIFY. No explanation, quotes, JSON, or Markdown."""


def messages_for(record):
    case = record["case"]
    return [{"role": "system", "content": POLICY},
            {"role": "user", "content": f"Explicit locale: {case['locale'] or 'not supplied'}.\nRequest: {case['text']}"}]


def parse_answer(raw, allow_fence=False):
    text = raw.strip()
    if allow_fence:
        match = re.fullmatch(r"```(?:[A-Za-z]+)?\n(.*?)\n```", text, re.S)
        if match:
            text = match[1].strip()
    if text == "CLARIFY":
        return "ambiguous"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        try:
            datetime.strptime(text, "%Y-%m-%d")
            return text
        except ValueError:
            pass
    return None


def score_answer(record, raw):
    case = record["case"]
    expected = date_context(case)[0]
    scores = {}
    for mode in ("strict", "fence_only"):
        selected = parse_answer(raw, allow_fence=mode == "fence_only")
        sandbox = replay(case, compile_date(case, selected)) if selected is not None else None
        committed = sandbox["final_state"]["committed"] if sandbox else None
        scores[mode] = {"parsed": selected is not None, "selected": selected, "correct": selected == expected,
                        "completed": sandbox["completion"] if sandbox else False,
                        "wrong_commit": committed is not None and committed["date"] != date_context(case)[1],
                        "unnecessary_clarification": selected == "ambiguous" and expected != "ambiguous",
                        "missed_clarification": selected is not None and selected != "ambiguous" and expected == "ambiguous",
                        "sandbox": sandbox}
    return scores


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", required=True)
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20261023)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("repeats must be positive")
    records = read_jsonl(args.cases)
    validate_cases([r["case"] for r in records])
    output = Path(args.output_dir)
    if not args.resume:
        output.mkdir(parents=True, exist_ok=False)
        (output / "cases.jsonl").write_bytes(Path(args.cases).read_bytes())
    import torch
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_num_threads(4)
    manifest = {"status": "started", "started_utc": datetime.now(timezone.utc).isoformat(),
                "model": "Qwen/Qwen3-0.6B", "revision": "c1899de289a04d12100db370d81485cdf75e47ca",
                "weights_sha256": sha256(Path(args.model_dir) / "model.safetensors"),
                "cases_sha256": sha256(args.cases), "collector_sha256": sha256(__file__),
                "service_scorer_sha256": sha256(Path(__file__).with_name("service_eval.py")),
                "adapter_sha256": sha256("experiments/build_attribution_cases.py"), "policy": POLICY,
                "python": platform.python_version(), "torch": torch.__version__, "transformers": transformers.__version__,
                "repeats": args.repeats, "seed": args.seed, "temperature": 0.7, "top_p": 0.8, "top_k": 20,
                "max_new_tokens": 48, "enable_thinking": False, "device": "cpu", "dtype": "float32", "threads": 4,
                "languages": sorted({r["case"]["language"] for r in records}),
                "design": "free-form scalar answers; fixed English policy; draft user-text translations; fixed workflow adapter"}
    if manifest["weights_sha256"] != "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b":
        raise ValueError("wrong model weights")
    path = output / "manifest.json"
    complete = set()
    if args.resume:
        previous = json.loads(path.read_text(encoding="utf-8"))
        if previous["status"] != "started":
            raise ValueError("run is not interrupted")
        for key in manifest:
            if key not in {"started_utc", "status"} and previous[key] != manifest[key]:
                raise ValueError(f"resume mismatch: {key}")
        indexed = {r["case"]["id"]: r for r in records}
        log = output / "attempts.jsonl"
        existing = read_jsonl(log) if log.exists() and log.stat().st_size else []
        for row in existing:
            key = row["id"], row["repeat"]
            if key in complete or row["repeat"] not in range(args.repeats):
                raise ValueError("duplicate or invalid saved repeat")
            if row["messages"] != messages_for(indexed[row["id"]]) or row["scores"] != score_answer(indexed[row["id"]], row["raw_output"]):
                raise ValueError("saved attempt mismatch")
            complete.add(key)
        previous.setdefault("resumes", []).append({"utc": datetime.now(timezone.utc).isoformat(), "preserved": len(existing),
                                                   "prefix_sha256": sha256(log) if existing else None})
        manifest = previous
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, trust_remote_code=False, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(args.model_dir, trust_remote_code=False, local_files_only=True,
                                               use_safetensors=True, torch_dtype=torch.float32)
    model.eval()
    jobs = [(r, repeat) for r in records for repeat in range(args.repeats)]
    random.Random(args.seed).shuffle(jobs)
    with (output / "attempts.jsonl").open("a" if args.resume else "x", encoding="utf-8") as log:
        for number, (record, repeat) in enumerate(jobs, 1):
            case = record["case"]
            if (case["id"], repeat) in complete:
                continue
            seed = int(hashlib.sha256(f"{args.seed}:{case['family']}:{case['locale']}:{repeat}".encode()).hexdigest()[:8], 16)
            torch.manual_seed(seed)
            messages = messages_for(record)
            rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
            inputs = tokenizer(rendered, return_tensors="pt")
            start = time.perf_counter()
            with torch.inference_mode():
                generated = model.generate(**inputs, max_new_tokens=48, do_sample=True, temperature=0.7,
                                           top_p=0.8, top_k=20, pad_token_id=tokenizer.eos_token_id)
            tokens = generated[0][inputs.input_ids.shape[-1]:]
            raw = tokenizer.decode(tokens, skip_special_tokens=True).strip()
            row = {"id": case["id"], "language": case["language"], "family": case["family"], "locale": case["locale"],
                   "date_kind": record["date_kind"], "repeat": repeat, "seed": seed, "messages": messages,
                   "prompt_sha256": hashlib.sha256(rendered.encode()).hexdigest(), "raw_output": raw,
                   "output_tokens": len(tokens), "latency_seconds": round(time.perf_counter() - start, 4),
                   "scores": score_answer(record, raw)}
            log.write(json.dumps(row, ensure_ascii=False) + "\n")
            log.flush()
            print(f"{number}/{len(jobs)} {case['id']} strict={row['scores']['strict']['correct']}", flush=True)
    manifest.update(status="completed", completed_utc=datetime.now(timezone.utc).isoformat(),
                    attempts_sha256=sha256(output / "attempts.jsonl"))
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
