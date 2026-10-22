"""Protect published research evidence without requiring model packages."""
import json
import random
import unittest
from pathlib import Path

from experiments.summarize_workflow import audit, summarize
from localesafe.evaluate import read_jsonl, sha256
from localesafe.workflow_probe import jobs_for, messages_for, score, seed_for

ROOT = Path(__file__).resolve().parents[1]


class WorkflowArchiveTests(unittest.TestCase):
    def test_study_card_matches_archived_results(self):
        from experiments.compare_workflow import render, study
        directories = [ROOT / f"experiments/results/workflow-gpu-qwen3-{tag}-20261022" for tag in ("06b", "17b")]
        self.assertEqual((ROOT / "docs/WORKFLOW_STUDY.md").read_text(encoding="utf-8"), render(study(directories)))

    def test_archived_bytes_and_partial_prefixes(self):
        directories = list((ROOT / "experiments/results").glob("workflow-*/archive-sha256.json"))
        self.assertGreaterEqual(len(directories), 2)
        for hashes_path in directories:
            directory = hashes_path.parent
            with self.subTest(directory=directory.name):
                for name, digest in json.loads(hashes_path.read_text(encoding="utf-8")).items():
                    self.assertEqual(sha256(directory / name), digest, name)
                manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
                if manifest["status"] == "completed":
                    _, records, rows = audit(directory)
                    saved = json.loads((directory / "summary.json").read_text(encoding="utf-8"))
                    self.assertEqual(summarize(records, rows), saved)
                    continue
                self.assertEqual(manifest["status"], "interrupted")
                settings = manifest["settings"]
                self.assertEqual(sha256(directory / "cases.jsonl"), settings["cases_sha256"])
                self.assertEqual(sha256(directory / "attempts.jsonl"), manifest["attempts_sha256"])
                records = read_jsonl(directory / "cases.jsonl")
                index = {r["id"]: r for r in records}
                rows = read_jsonl(directory / "attempts.jsonl")
                jobs = jobs_for(records, settings["repeats"])
                random.Random(settings["seed"]).shuffle(jobs)
                self.assertEqual(len(rows), manifest["recorded_attempts"])
                self.assertLess(len(rows), len(jobs))
                for row, job in zip(rows, jobs):
                    self.assertEqual((row["id"], row["condition"], row["repeat"]), job)
                    record = index[row["id"]]
                    self.assertEqual(row["seed"], seed_for(record["scenario"], row["condition"], row["repeat"], settings["seed"]))
                    self.assertEqual(row["messages"], messages_for(record, row["condition"]))
                    self.assertEqual(row["scores"], score(record, row["condition"], row["raw_output"]))
