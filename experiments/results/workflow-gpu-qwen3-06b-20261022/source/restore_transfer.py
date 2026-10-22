"""Restore a compact transfer only if every original raw-file SHA-256 matches."""
import argparse
import hashlib
import json
import random
from pathlib import Path

from localesafe.evaluate import read_jsonl, sha256
from localesafe.workflow_probe import jobs_for, messages_for, score, seed_for


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transfer", type=Path)
    parser.add_argument("--cases", type=Path, default=Path("experiments/workflow/cases.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("reports"))
    args = parser.parse_args()
    from transformers import AutoTokenizer
    payload = json.loads(args.transfer.read_text(encoding="utf-8"))
    records = read_jsonl(args.cases)
    indexed = {record["id"]: record for record in records}
    restored = []
    for tag, data in payload["runs"].items():
        manifest = json.loads(data["manifest_text"])
        settings = manifest["settings"]
        if settings["cases_sha256"] != sha256(args.cases):
            raise ValueError("case hash mismatch")
        tokenizer = AutoTokenizer.from_pretrained(Path("private") / tag, local_files_only=True, trust_remote_code=False)
        jobs = jobs_for(records, settings["repeats"])
        random.Random(settings["seed"]).shuffle(jobs)
        if len(jobs) != len(data["output_indices"]) or len(jobs) != len(data["output_tokens"]):
            raise ValueError("incomplete transfer")
        lines = []
        for i, (ident, condition, repeat) in enumerate(jobs):
            record = indexed[ident]
            messages = messages_for(record, condition)
            rendered = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
            raw = data["outputs"][data["output_indices"][i]]
            row = {"id": ident, "scenario": record["scenario"], "language": record["language"], "family": record["family"],
                   "condition": condition, "repeat": repeat, "seed": seed_for(record["scenario"], condition, repeat, settings["seed"]),
                   "messages": messages, "prompt_sha256": hashlib.sha256(rendered.encode()).hexdigest(), "raw_output": raw,
                   "output_tokens": data["output_tokens"][i], "batch_index": i // settings["batch_size"],
                   "batch_latency_seconds": data["batch_latencies"][i // settings["batch_size"]], "scores": score(record, condition, raw)}
            lines.append(json.dumps(row, ensure_ascii=False) + "\n")
        raw_bytes = "".join(lines).encode("utf-8")
        if hashlib.sha256(raw_bytes).hexdigest() != manifest["attempts_sha256"]:
            raise ValueError(f"restored raw file differs from original: {tag}")
        restored.append((tag, data["manifest_text"].encode("utf-8"), raw_bytes))
    for tag, manifest_bytes, raw_bytes in restored:
        directory = args.output / ("workflow-gpu-" + tag)
        directory.mkdir(parents=True, exist_ok=False)
        (directory / "manifest.json").write_bytes(manifest_bytes)
        (directory / "attempts.jsonl").write_bytes(raw_bytes)
        (directory / "cases.jsonl").write_bytes(args.cases.read_bytes())
        print(f"{tag}: original raw-file SHA-256 verified; all 900 records restored")


if __name__ == "__main__":
    main()
