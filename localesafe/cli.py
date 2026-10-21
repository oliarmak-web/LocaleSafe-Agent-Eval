"""Offline CLI. Input files are data; tool calls are never executed."""

import argparse
import json
import platform
from pathlib import Path

from . import __version__
from .evaluate import evaluate, read_jsonl, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", required=True)
    parser.add_argument("--responses", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--run-label", required=True, help="Record model/version or explicitly label synthetic fixtures")
    args = parser.parse_args()
    try:
        report = evaluate(read_jsonl(args.cases), read_jsonl(args.responses))
        report["provenance"] = {"runner_version": __version__, "python": platform.python_version(),
                                "run_label": args.run_label, "cases_sha256": sha256(args.cases),
                                "responses_sha256": sha256(args.responses)}
        path = Path(args.output)
        if path.resolve() in {Path(args.cases).resolve(), Path(args.responses).resolve()}:
            raise ValueError("output must not overwrite inputs")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as output:
            json.dump(report, output, indent=2, ensure_ascii=False, allow_nan=False)
            output.write("\n")
    except (ValueError, OSError, TypeError) as exc:
        parser.exit(2, f"error: {exc}\n")
    print(f"Evaluated {report['n']} cases. Report: {path}")


if __name__ == "__main__":
    main()
