import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from experiments.build_workflow_cases import build
from experiments.summarize_workflow import audit, summarize
from localesafe.evaluate import sha256
from localesafe.workflow_probe import jobs_for, messages_for, score, seed_for


def canonical_rows(records):
    rows = []
    for ident, condition, repeat in jobs_for(records, 1):
        record = next(r for r in records if r["id"] == ident)
        raw = json.dumps(record["recovery_expected"] if condition == "recovery" else record["expected"])
        rows.append({"id": ident, "scenario": record["scenario"], "family": record["family"], "language": record["language"],
                     "condition": condition, "repeat": repeat, "seed": seed_for(record["scenario"], condition, repeat, 42),
                     "messages": messages_for(record, condition), "raw_output": raw, "output_tokens": 20,
                     "scores": score(record, condition, raw)})
    return rows


class WorkflowSummaryTests(unittest.TestCase):
    def test_shared_controls_and_pair_denominators(self):
        records = build()
        result = summarize(records, canonical_rows(records))["strict"]
        self.assertEqual(result["conditions"]["baseline"]["n"], 150)
        self.assertEqual(result["conditions"]["structured_facts"]["n"], 30)
        self.assertEqual(result["contrasts"]["english_vs_target"]["uk"]["pairs"], 30)
        self.assertEqual(result["contrasts"]["baseline_vs_structured_facts"]["uk"]["both_correct"], 30)

    def test_audit_rejects_prompt_and_hash_tampering(self):
        import random
        records = build()[:5]  # One matched scenario in five languages.
        rows = canonical_rows(records)
        order = jobs_for(records, 1)
        random.Random(42).shuffle(order)
        index = {(r["id"], r["condition"], r["repeat"]): r for r in rows}
        rows = [index[key] for key in order]
        for i, row in enumerate(rows):
            row["batch_index"] = i // 4
        with TemporaryDirectory() as directory:
            path = Path(directory)
            (path / "cases.jsonl").write_text("".join(json.dumps(r) + "\n" for r in records))
            def save():
                (path / "attempts.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
                manifest = {"status": "completed", "attempts": len(rows), "attempts_sha256": sha256(path / "attempts.jsonl"),
                            "settings": {"cases_sha256": sha256(path / "cases.jsonl"), "repeats": 1, "seed": 42, "batch_size": 4}}
                (path / "manifest.json").write_text(json.dumps(manifest))
            save()
            self.assertEqual(len(audit(path)[2]), 15)
            rows[0]["messages"][-1]["content"] += " injected"
            save()  # Hash alone passes; reconstructed prompt must fail.
            with self.assertRaisesRegex(ValueError, "prompt/score"):
                audit(path)
            (path / "attempts.jsonl").write_text("{}\n")
            with self.assertRaisesRegex(ValueError, "hash"):
                audit(path)
