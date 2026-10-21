import itertools
import json
import random
import tempfile
import unittest
from pathlib import Path

from experiments.summarize_attribution import audit, summarize
from localesafe.attribution_probe import assess, paired_seed, prompt_for
from localesafe.evaluate import read_jsonl, sha256

ROOT = Path(__file__).resolve().parents[1]


class AttributionSummaryTests(unittest.TestCase):
    def test_complete_audit_and_tamper_detection(self):
        tasks = read_jsonl(ROOT / "experiments/attribution/tasks.jsonl")
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            (directory / "tasks.jsonl").write_bytes((ROOT / "experiments/attribution/tasks.jsonl").read_bytes())
            rows = []
            for task in tasks:
                case = task["case"]
                for order in itertools.permutations(range(3)):
                    seed = paired_seed(task, order, 0, 42)
                    label = random.Random(seed).choices(range(3), weights=[1/3]*3, k=1)[0]
                    option = order[label]
                    rows.append({"id": case["id"], "kind": task["kind"], "family": case["family"],
                                 "locale": case["locale"], "language": case["language"], "phrase": task["phrase"],
                                 "order": list(order), "draw": 0, "seed": seed, "probabilities_ABC": [1/3]*3,
                                 "chosen_label": "ABC"[label], "selected_option": option, "score": assess(task, option),
                                 "messages": prompt_for(task, order)})
            log = directory / "attempts.jsonl"
            log.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
            manifest = {"status": "completed", "model": "synthetic-unit-test", "draws_per_order": 1, "seed": 42,
                        "attempts_sha256": sha256(log), "tasks_sha256": sha256(directory / "tasks.jsonl")}
            (directory / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            report = summarize(directory)
            self.assertEqual(report["oracle_controls"]["passed"], 30)
            self.assertAlmostEqual(report["workflow"]["mean_probability_correct"], 1/3)
            rows[0]["score"]["passed"] = not rows[0]["score"]["passed"]
            log.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
            manifest["attempts_sha256"] = sha256(log)
            (directory / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "score mismatch"):
                audit(directory)
