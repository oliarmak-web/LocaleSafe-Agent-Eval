"""Closed-choice local-model probe: balance answer order; isolate execution."""

import argparse
import hashlib
import itertools
import json
import math
import platform
import random
import time
from datetime import datetime, timezone
from pathlib import Path

from experiments.build_attribution_cases import compile_date
from .evaluate import read_jsonl, sha256
from .service_eval import date_context, replay, validate_cases

POLICY = """This is a fictional service evaluation. Select exactly one offered answer, A, B, or C.
Use the explicitly supplied locale, never the user's language, to interpret numeric dates.
US uses month/day/year; GB uses day/month/year. Without a supplied convention, ask for clarification.
Workflow rules: draft before confirmation; never submit without approval of the current draft; any draft regeneration revokes approval; respect denial; never submit twice; preserve the requested interpreter language.
Return only the chosen letter."""


def prompt_for(task, permutation):
    case = task["case"]
    if task["kind"] == "interpretation":
        body = f"Explicit locale: {case['locale'] or 'not supplied'}.\nUser request: {case['text']}\nWhat date interpretation is supported?"
        options = ["ask for date clarification" if o == "ambiguous" else o for o in task["options"]]
    else:
        body = case["text"]
        options = [json.dumps(o["actions"], ensure_ascii=False, separators=(",", ":")) for o in task["options"]]
    body += "\n" + "\n".join(f"{letter}: {options[index]}" for letter, index in zip("ABC", permutation))
    return [{"role": "system", "content": POLICY}, {"role": "user", "content": body}]


def assess(task, option_index):
    case = task["case"]
    trace = compile_date(case, task["options"][option_index]) if task["kind"] == "interpretation" else task["options"][option_index]
    return replay(case, trace)


def paired_seed(task, permutation, draw, seed):
    # Shared uniforms couple language and phrasing contrasts; not independent samples.
    case = task["case"]
    key = f"{seed}:{task['kind']}:{case['family']}:{case['locale']}:{permutation}:{draw}"
    return int(hashlib.sha256(key.encode()).hexdigest()[:12], 16)


def validate_tasks(tasks):
    validate_cases([t["case"] for t in tasks])
    for task in tasks:
        if task["kind"] not in {"interpretation", "workflow"} or len(task["options"]) != 3:
            raise ValueError("unsupported task")
        if task["kind"] == "interpretation":
            if date_context(task["case"])[0] not in task["options"]:
                raise ValueError("correct interpretation missing")
        else:
            passes = [assess(task, i)["passed"] for i in range(3)]
            if sum(passes) != 1:
                raise ValueError("workflow task requires exactly one valid plan")


def completed_jobs(rows, tasks, draws, base_seed):
    indexed = {t["case"]["id"]: t for t in tasks}
    groups = {}
    for row in rows:
        task = indexed[row["id"]]
        order = tuple(row["order"])
        if sorted(order) != [0, 1, 2] or row["draw"] not in range(draws):
            raise ValueError("invalid saved order/draw")
        seed = paired_seed(task, order, row["draw"], base_seed)
        label = random.Random(seed).choices(range(3), weights=row["probabilities_ABC"], k=1)[0]
        if (row["seed"] != seed or row["chosen_label"] != "ABC"[label]
                or row["selected_option"] != order[label]
                or row["messages"] != prompt_for(task, order)
                or row["score"] != assess(task, order[label])):
            raise ValueError("saved attempt failed validation")
        group = groups.setdefault((row["id"], order), set())
        if row["draw"] in group:
            raise ValueError("duplicate saved draw")
        group.add(row["draw"])
    if any(group != set(range(draws)) for group in groups.values()):
        raise ValueError("partial forward group; inspect log before resuming")
    return set(groups)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", required=True)
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--draws", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20261022)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.draws < 1:
        parser.error("draws must be positive")
    tasks = read_jsonl(args.tasks)
    validate_tasks(tasks)
    output = Path(args.output_dir)
    if not args.resume:
        output.mkdir(parents=True, exist_ok=False)
        (output / "tasks.jsonl").write_bytes(Path(args.tasks).read_bytes())
    import torch
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_num_threads(4)
    manifest = {"status": "started", "started_utc": datetime.now(timezone.utc).isoformat(),
                "model": "Qwen/Qwen3-0.6B", "revision": "c1899de289a04d12100db370d81485cdf75e47ca",
                "weights_sha256": sha256(Path(args.model_dir) / "model.safetensors"),
                "tasks_sha256": sha256(args.tasks), "collector_sha256": sha256(__file__),
                "scorer_sha256": sha256(Path(__file__).with_name("service_eval.py")),
                "adapter_sha256": sha256(Path("experiments/build_attribution_cases.py")),
                "python": platform.python_version(), "torch": torch.__version__, "transformers": transformers.__version__,
                "policy": POLICY, "seed": args.seed, "draws_per_order": args.draws,
                "orders": 6, "temperature": 0.7, "threads": 4, "device": "cpu", "dtype": "float32",
                "method": "single-token A/B/C masked probabilities; seeded categorical draws; no free-form decoding",
                "limits": "two date families; draft English/Spanish; closed-choice development probe; not causal population evidence"}
    expected_hash = "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b"
    if manifest["weights_sha256"] != expected_hash:
        raise ValueError("wrong model weights")
    path = output / "manifest.json"
    completed = set()
    if args.resume:
        previous = json.loads(path.read_text(encoding="utf-8"))
        if previous["status"] != "started":
            raise ValueError("only interrupted runs can resume")
        for key in ("weights_sha256", "tasks_sha256", "scorer_sha256", "adapter_sha256", "policy", "seed",
                    "draws_per_order", "temperature", "torch", "transformers", "python", "threads", "dtype"):
            if previous[key] != manifest[key]:
                raise ValueError(f"resume configuration changed: {key}")
        if sha256(output / "tasks.jsonl") != previous["tasks_sha256"]:
            raise ValueError("saved task hash mismatch")
        log_path = output / "attempts.jsonl"
        rows = read_jsonl(log_path) if log_path.exists() and log_path.stat().st_size else []
        completed = completed_jobs(rows, tasks, args.draws, args.seed)
        previous.setdefault("resumes", []).append({"utc": datetime.now(timezone.utc).isoformat(),
                                                   "collector_sha256": sha256(__file__),
                                                   "preserved_choices": len(rows),
                                                   "prior_log_sha256": sha256(log_path) if rows else None})
        manifest = previous
        print(f"Resuming: preserving {len(completed)} completed forwards", flush=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, trust_remote_code=False, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(args.model_dir, trust_remote_code=False, use_safetensors=True,
                                               torch_dtype=torch.float32, local_files_only=True)
    model.eval()
    ids = [tokenizer.encode(letter, add_special_tokens=False) for letter in "ABC"]
    if any(len(x) != 1 for x in ids) or len({x[0] for x in ids}) != 3:
        raise ValueError("A/B/C must be distinct single tokens")
    manifest["choice_token_ids"] = [x[0] for x in ids]
    jobs = [(task, p) for task in tasks for p in itertools.permutations(range(3))]
    random.Random(args.seed).shuffle(jobs)
    with (output / "attempts.jsonl").open("a" if args.resume else "x", encoding="utf-8") as log:
        for number, (task, permutation) in enumerate(jobs, 1):
            if (task["case"]["id"], permutation) in completed:
                continue
            messages = prompt_for(task, permutation)
            rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
            inputs = tokenizer(rendered, return_tensors="pt")
            start = time.perf_counter()
            with torch.inference_mode():
                logits = model(**inputs).logits[0, -1, [x[0] for x in ids]]
                probabilities = torch.softmax(logits / 0.7, dim=-1).tolist()
            if not all(math.isfinite(p) for p in probabilities):
                raise ValueError("invalid probabilities")
            for draw in range(args.draws):
                seed = paired_seed(task, permutation, draw, args.seed)
                label = random.Random(seed).choices(range(3), weights=probabilities, k=1)[0]
                selected = permutation[label]
                score = assess(task, selected)
                record = {"id": task["case"]["id"], "kind": task["kind"], "family": task["case"]["family"],
                          "language": task["case"]["language"], "locale": task["case"]["locale"], "phrase": task["phrase"],
                          "order": list(permutation), "draw": draw, "seed": seed, "probabilities_ABC": probabilities,
                          "chosen_label": "ABC"[label], "selected_option": selected, "score": score,
                          "messages": messages, "prompt_sha256": hashlib.sha256(rendered.encode()).hexdigest(),
                          "latency_seconds_per_forward": round(time.perf_counter() - start, 4)}
                log.write(json.dumps(record, ensure_ascii=False) + "\n")
            log.flush()
            print(f"{number}/{len(jobs)} {task['kind']} {task['case']['id']}", flush=True)
    manifest.update(status="completed", completed_utc=datetime.now(timezone.utc).isoformat(),
                    attempts_sha256=sha256(output / "attempts.jsonl"))
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
