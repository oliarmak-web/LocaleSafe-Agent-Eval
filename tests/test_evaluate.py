import copy
import unittest
from pathlib import Path

from localesafe.evaluate import evaluate, read_jsonl

ROOT = Path(__file__).resolve().parents[1]


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.cases = read_jsonl(ROOT / "examples/cases.jsonl")
        self.responses = read_jsonl(ROOT / "examples/synthetic-perfect.jsonl")

    def test_perfect_and_injected_failures(self):
        perfect = evaluate(self.cases, self.responses)
        self.assertTrue(all(r["passed"] for r in perfect["cases"]))
        faulty = evaluate(self.cases, read_jsonl(ROOT / "examples/synthetic-failures.jsonl"))
        self.assertEqual(sum(not r["passed"] for r in faulty["cases"]), 3)
        self.assertEqual(faulty["languages"]["es"]["missed_escalations"], 1)
        self.assertEqual(faulty["languages"]["uk"]["unnecessary_escalations"], 1)
        self.assertAlmostEqual(faulty["paired_gaps"]["uk"]["english_minus_language_pass_rate"], 2/6)

    def test_missing_duplicate_and_unknown_responses_fail_closed(self):
        for rows in (self.responses[:-1], self.responses + [self.responses[0]],
                     self.responses + [{"id": "unknown", "decision": "respond", "tool_calls": []}]):
            with self.assertRaises(ValueError):
                evaluate(self.cases, rows)

    def test_pair_cannot_leak_across_splits(self):
        self.cases[1]["split"] = "test"
        with self.assertRaises(ValueError):
            evaluate(self.cases, self.responses)

    def test_extra_and_duplicate_calls_are_failures(self):
        changed = copy.deepcopy(self.responses)
        changed[0]["tool_calls"] *= 2
        self.assertFalse(evaluate(self.cases, changed)["cases"][0]["tools_exact"])

    def test_argument_key_order_is_irrelevant(self):
        self.responses[0]["tool_calls"][0]["arguments"] = {"priority": "urgent", "location": "B14"}
        self.assertTrue(evaluate(self.cases, self.responses)["cases"][0]["passed"])

    def test_invalid_decisions_and_calls_rejected(self):
        for value in ("unknown", None, True):
            changed = copy.deepcopy(self.responses)
            changed[0]["decision"] = value
            with self.assertRaises(ValueError):
                evaluate(self.cases, changed)
        self.responses[0]["tool_calls"] = [{"name": "x", "arguments": "not an object"}]
        with self.assertRaises(ValueError):
            evaluate(self.cases, self.responses)


if __name__ == "__main__":
    unittest.main()
