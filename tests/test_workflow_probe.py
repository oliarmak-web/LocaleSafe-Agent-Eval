import json
import unittest

from experiments.build_workflow_cases import build
from localesafe.workflow_probe import execute, jobs_for, messages_for, parse, score, seed_for


class WorkflowProbeTests(unittest.TestCase):
    def test_matched_grid_and_canonical_calls(self):
        records = build()
        self.assertEqual(len(records), 150)
        self.assertEqual(len(jobs_for(records, 2)), 900)
        grouped = {}
        for record in records:
            grouped.setdefault(record["scenario"], []).append(record)
            for condition in ("baseline", "localized_policy", "structured_facts", "recovery"):
                expected = record["recovery_expected"] if condition == "recovery" else record["expected"]
                self.assertTrue(score(record, condition, json.dumps(expected))["strict"]["completed"])
        self.assertEqual(len(grouped), 30)
        for group in grouped.values():
            for field in ("context", "facts", "expected", "injected_proposal", "recovery_expected"):
                self.assertTrue(all(r[field] == group[0][field] for r in group))

    def test_unauthorized_mutation_blocked_but_counted(self):
        context = build()[0]["context"]
        for action in ({"tool": "commit"}, {"tool": "cancel", "id": "A1"}):
            result = execute(context, action)
            self.assertTrue(result["unauthorized_attempt"])
            self.assertFalse(result["executed"])
            self.assertIsNone(result["state"]["committed"])

    def test_valid_execution_can_be_wrong(self):
        record = next(r for r in build() if r["family"] == "correction")
        scorecard = score(record, "baseline", json.dumps(record["injected_proposal"]))["strict"]
        self.assertTrue(scorecard["execution"]["executed"])
        self.assertFalse(scorecard["completed"])
        self.assertFalse(scorecard["correct_action"])

    def test_unavailable_slot_rejected(self):
        record = next(r for r in build() if r["family"] == "unavailable")
        slot = next(s["id"] for s in record["context"]["slots"] if not s["available"])
        action = {**record["expected"], "slot": slot}
        self.assertFalse(execute(record["context"], action)["executed"])

    def test_gold_and_facts_not_in_baseline_prompt(self):
        record = build()[0]
        message = messages_for(record, "baseline")[-1]["content"]
        self.assertNotIn('"expected"', message)
        self.assertNotIn('Verified user facts:', message)
        self.assertNotIn('"intent"', message)
        self.assertIn('Verified user facts:', messages_for(record, "structured_facts")[-1]["content"])

    def test_parser_cannot_repair_or_ignore_duplicate_keys(self):
        raw = '{"tool":"lookup","id":"A1"}'
        self.assertEqual(parse(raw), {"tool": "lookup", "id": "A1"})
        self.assertIsNone(parse('```json\n' + raw + '\n```'))
        self.assertEqual(parse('```json\n' + raw + '\n```', True), parse(raw))
        for invalid in ('{"tool":"lookup","id":"A1","id":"A2"}', raw + ' explanation', '[]', '{"tool":"lookup","id":1}'):
            self.assertIsNone(parse(invalid, True))

    def test_matched_seed_and_rejected_proposal_history(self):
        self.assertEqual(seed_for("x", "baseline", 0, 42), seed_for("x", "localized_policy", 0, 42))
        messages = messages_for(build()[0], "recovery")
        self.assertEqual([r["role"] for r in messages], ["system", "user", "assistant", "user"])
        self.assertIn('I reject', messages[-1]["content"])
