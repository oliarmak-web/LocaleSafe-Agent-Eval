import unittest

from localesafe.collect_local import messages_for, parse_prediction, summarize_attempts
from localesafe.evaluate import read_jsonl
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.cases = read_jsonl(ROOT / "examples/cases.jsonl")

    def test_prompt_does_not_include_gold(self):
        case = dict(self.cases[0], expected={"secret_gold": "DO_NOT_LEAK"})
        prompt = str(messages_for(case, "baseline"))
        self.assertNotIn("DO_NOT_LEAK", prompt)
        self.assertNotIn(case["id"], prompt)
        self.assertEqual(messages_for(case, "check")[1]["content"], case["text"])

    def test_strict_generation_validation(self):
        prediction = parse_prediction('{"decision":"respond","tool_calls":[]}', self.cases[0])
        self.assertEqual(prediction["decision"], "respond")
        for text in ('```json\n{}\n```', '{"decision":"bad","tool_calls":[]}', '{}'):
            with self.assertRaises(ValueError):
                parse_prediction(text, self.cases[0])

    def test_invalid_attempts_remain_in_denominator(self):
        attempts = [{"id": c["id"], "prediction": {"id": c["id"], **c["expected"]}} for c in self.cases]
        attempts[0].pop("prediction")
        report = summarize_attempts(self.cases, attempts)
        self.assertEqual(report["n"], 18)
        self.assertEqual(report["invalid_generations"], 1)
        self.assertAlmostEqual(report["languages"]["en"]["pass_rate"], 5/6)
        self.assertEqual(report["languages"]["en"]["missed_escalations"], 0)
        self.assertFalse(report["cases"][0]["generation_valid"])

    def test_incomplete_attempts_rejected(self):
        with self.assertRaises(ValueError):
            summarize_attempts(self.cases, [])
