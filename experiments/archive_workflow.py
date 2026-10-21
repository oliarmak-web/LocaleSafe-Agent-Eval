"""Audit and archive a completed workflow experiment without rewriting raw data."""
import argparse
import json
import shutil
from pathlib import Path

from experiments.summarize_workflow import audit, report, summarize
from localesafe.evaluate import sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    manifest, records, rows = audit(args.run)
    gpu = manifest["settings"]["device"] == "cuda"
    sources = {"collector.py": "localesafe/workflow_gpu.py" if gpu else "localesafe/workflow_probe.py", "build_cases.py": "experiments/build_workflow_cases.py",
               "summarize.py": "experiments/summarize_workflow.py", "archive.py": __file__}
    if gpu:
        sources["shared_scorer.py"] = "localesafe/workflow_probe.py"
        if sha256(sources["shared_scorer.py"]) != manifest["settings"]["shared_scorer_sha256"]:
            raise ValueError("shared scorer changed")
    if sha256(sources["collector.py"]) != manifest["settings"]["collector_sha256"] or sha256(sources["build_cases.py"]) != manifest["settings"]["builder_sha256"]:
        raise ValueError("collection source changed; locate original snapshot before archiving")
    args.destination.mkdir(parents=True, exist_ok=False)
    for name in ("manifest.json", "cases.jsonl", "attempts.jsonl"):
        shutil.copyfile(args.run / name, args.destination / name)
    summary = summarize(records, rows)
    (args.destination / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (args.destination / "RESULTS.md").write_text(report(manifest, summary), encoding="utf-8")
    (args.destination / "source").mkdir()
    for name, path in sources.items():
        shutil.copyfile(path, args.destination / "source" / name)
    shutil.copyfile("experiments/workflow/PROTOCOL.md", args.destination / "PROTOCOL.md")
    shutil.copyfile("experiments/runtime-versions.txt", args.destination / "runtime-versions.txt")
    model_dir = Path("private") / ("qwen3-17b" if "1.7B" in manifest["settings"]["model"]["model"] else "qwen3-06b")
    provenance = {p.name: sha256(p) for p in model_dir.iterdir() if p.is_file() and p.suffix in {".json", ".txt", ".jinja"}}
    (args.destination / "model-config-sha256.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    hashes = {p.relative_to(args.destination).as_posix(): sha256(p) for p in args.destination.rglob("*") if p.is_file()}
    (args.destination / "archive-sha256.json").write_text(json.dumps(hashes, indent=2) + "\n", encoding="utf-8")
    print(f"Archived {len(rows)} audited generations to {args.destination}")


if __name__ == "__main__":
    main()
