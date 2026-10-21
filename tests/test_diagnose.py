import json
import unittest
from pathlib import Path

from localesafe.diagnose import diagnose
from localesafe.evaluate import read_jsonl

ROOT = Path(__file__).resolve().parents[1]


class DiagnosisTests(unittest.TestCase):
    def test_shared_errors_and_language_disagreements_are_separate(self):
        cases = read_jsonl(ROOT / "examples/cases.jsonl")
        attempts = [{"id": c["id"], "condition": "baseline", "prediction": {"id": c["id"], **c["expected"]}}
                    for c in cases]
        # Spanish-only decision error, then a shared English/Spanish decision error.
        for index in (1, 3, 4):
            attempts[index]["prediction"] = {"id": cases[index]["id"], "decision": "clarify", "tool_calls": []}
        pairs = diagnose(cases, attempts)["conditions"]["baseline"]["strict"]["paired_with_english"]["es"]
        self.assertEqual(pairs["english_pass_other_fail"], 1)
        self.assertEqual(pairs["both_fail"], 1)
        self.assertEqual(pairs["english_decision_correct_other_wrong"], 1)

    def test_format_failure_is_not_invented_decision_error(self):
        cases = read_jsonl(ROOT / "examples/cases.jsonl")
        attempts = [{"id": c["id"], "condition": "baseline", "prediction": {"id": c["id"], **c["expected"]}}
                    for c in cases]
        attempts[1].pop("prediction")
        attempts[1]["raw_output"] = "```json\n" + json.dumps(cases[1]["expected"]) + "\n```"
        result = diagnose(cases, attempts)["conditions"]["baseline"]
        strict = result["strict"]["languages"]["es"]
        self.assertEqual(strict["format_failures"], 1)
        self.assertEqual(strict["decision_errors_among_parseable"], 0)
        self.assertEqual(result["fence_only_posthoc"]["languages"]["es"]["format_failures"], 0)
