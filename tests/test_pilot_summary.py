import json
import tempfile
import unittest
from pathlib import Path

from experiments.summarize_pilot import summarize
from localesafe.collect_local import summarize_attempts
from localesafe.evaluate import read_jsonl, sha256

ROOT = Path(__file__).resolve().parents[1]


class SummaryTests(unittest.TestCase):
    def test_summary_requires_completed_untampered_artifacts(self):
        cases = read_jsonl(ROOT / "examples/cases.jsonl")
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            rows = [{"id": c["id"], "condition": condition, "latency_seconds": 1,
                     "prediction": {"id": c["id"], **c["expected"]}}
                    for condition in ("baseline", "check") for c in cases]
            log = directory / "attempts.jsonl"
            log.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
            manifest = {"status": "completed", "model": "synthetic-test-only", "revision": "test",
                        "completed_utc": "test", "attempts_sha256": sha256(log)}
            (directory / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            for condition in ("baseline", "check"):
                report = summarize_attempts(cases, [r for r in rows if r["condition"] == condition])
                (directory / f"{condition}-report.json").write_text(json.dumps(report), encoding="utf-8")
            summarize(directory)
            self.assertIn("18/18", (directory / "RESULTS.md").read_text(encoding="utf-8"))
            log.write_text("changed", encoding="utf-8")
            with self.assertRaises(ValueError):
                summarize(directory)
