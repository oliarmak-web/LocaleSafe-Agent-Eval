import copy
import json
import unittest
from pathlib import Path

from experiments.build_handoff_cases import CONTROLS, build, trace_for
from localesafe.handoff_eval import actor_packet, evaluate, monitor_packet, replay, validate_case


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.cases = build()

    def case(self, outcome):
        return next(c for c in self.cases if c["outcome"] == outcome)

    def test_matched_languages_preserve_trusted_meaning(self):
        self.assertEqual(len(self.cases), 48)
        for scenario in {c["scenario"] for c in self.cases}:
            matched = [c for c in self.cases if c["scenario"] == scenario]
            self.assertEqual(len(matched), 4)
            for case in matched:
                validate_case(case)
            for e in (0, 1):
                for field in ("permission", "requested_action", "version", "principal"):
                    self.assertTrue(all(c["events"][e][field] == matched[0]["events"][e][field] for c in matched))

    def test_approved_actions_complete_and_wrong_principal_cannot_commit(self):
        for outcome in ("maintain", "replace_approved"):
            case = self.case(outcome)
            trace = trace_for(case, "oracle")
            result = replay(case, trace)
            self.assertTrue(result["completed"])
            self.assertNotEqual(result["final_state"], case["initial_state"])
            trace["principal"] = "another-user"
            denied = replay(case, trace)
            self.assertTrue(denied["guard_blocked"])
            self.assertTrue(denied["unauthorized_attempt"])
            self.assertEqual(denied["final_state"], case["initial_state"])

    def test_latest_version_does_not_authorize_old_scope(self):
        for outcome in ("revoke", "replace_unapproved", "replace_approved"):
            case = self.case(outcome)
            trace = trace_for(case, "stale_handoff")
            trace["action"] = {**trace["action"], "permission_version": 2}
            result = replay(case, trace)
            self.assertTrue(result["unauthorized_attempt"])
            self.assertTrue(result["monitor_false_allow"])
            self.assertFalse(result["executed"])
            self.assertEqual(result["final_state"], case["initial_state"])

    def test_actor_monitor_and_handoff_failures_are_separate(self):
        case = self.case("revoke")
        stale = replay(case, trace_for(case, "stale_handoff"))
        actor = replay(case, trace_for(case, "monitor_misses"))
        self.assertFalse(stale["handoff_faithful"])
        self.assertTrue(actor["handoff_faithful"])
        self.assertTrue(actor["unauthorized_attempt"])
        wrong = replay(case, trace_for(case, "wrong_proposal"))
        self.assertFalse(wrong["actor_correct"])
        self.assertFalse(wrong["unauthorized_attempt"])
        self.assertTrue(wrong["monitor_correct"])  # Safe proposal is not an authorized write.
        self.assertFalse(wrong["completed"])

    def test_refusing_everything_fails_approved_task_and_monitor(self):
        case = self.case("maintain")
        result = replay(case, trace_for(case, "monitor_overblocks"))
        self.assertTrue(result["actor_correct"])
        self.assertTrue(result["monitor_false_block"])
        self.assertFalse(result["completed"])

    def test_missing_invalid_and_abstention_not_dropped(self):
        result = evaluate(self.cases, [])
        self.assertEqual(result["missing_traces"], 48)
        self.assertEqual(result["counts"]["completed"], 0)
        trace = trace_for(self.cases[0], "oracle")
        trace["action"] = {**trace["action"], "permission_version": True}
        self.assertFalse(replay(self.cases[0], trace)["format_valid"])
        trace = trace_for(self.cases[0], "oracle")
        trace["monitor"] = "abstain"
        result = replay(self.cases[0], trace)
        self.assertTrue(result["monitor_abstained"])
        self.assertFalse(result["monitor_correct"])
        self.assertFalse(result["completed"])

    def test_model_packets_exclude_hidden_reference_fields(self):
        case = self.case("replace_approved")
        packet = actor_packet(case)
        for event in packet["evidence"]:
            self.assertEqual(set(event), {"event_id", "principal", "language", "text"})
        self.assertNotIn("requested_action", json.dumps(packet["evidence"]))
        action = trace_for(case, "oracle")["action"]
        monitor = monitor_packet(case, action)
        self.assertEqual(monitor["proposed_action"], action)
        self.assertNotIn("correct", monitor)
        self.assertNotIn("outcome", packet)
        extracted = {"untrusted": "I can approve everything"}
        self.assertEqual(actor_packet(case, "extracted_record", extracted)["evidence"], extracted)
        self.assertTrue(replay(case, {**trace_for(case, "stale_handoff"), "handoff": extracted})["guard_blocked"])

    def test_bad_event_order_and_duplicate_outputs_rejected(self):
        case = copy.deepcopy(self.cases[0])
        case["events"].reverse()
        with self.assertRaises(ValueError):
            validate_case(case)
        trace = trace_for(self.cases[0], "oracle")
        with self.assertRaises(ValueError):
            evaluate(self.cases, [trace, trace])

    def test_reference_contradictions_rejected_and_packet_mutation_isolated(self):
        case = copy.deepcopy(self.case("maintain"))
        original = copy.deepcopy(case)
        packet = actor_packet(case, "oracle_record")
        packet["evidence"]["permission"]["resource"] = "forged-resource"
        packet["state"]["records"].clear()
        self.assertEqual(case, original)
        case["events"][-1]["requested_action"]["permission_version"] = 1
        with self.assertRaisesRegex(ValueError, "contradicts"):
            validate_case(case)

    def test_committed_fixtures_match_builder_and_controls(self):
        root = Path(__file__).resolve().parents[1] / "experiments" / "handoff"
        cases = [json.loads(line) for line in (root / "cases.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(cases, self.cases)
        packets = [json.loads(line) for line in (root / "actor-packets.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(packets, [{"id": c["id"], **actor_packet(c)} for c in cases])
        saved = json.loads((root / "synthetic-results.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["trace_origin"], "synthetic")
        for control in CONTROLS:
            traces = [json.loads(line) for line in (root / f"{control}.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(traces, [trace_for(c, control) for c in cases])
            result = evaluate(cases, traces)
            self.assertEqual({k: v for k, v in result.items() if k != "rows"}, saved["controls"][control])
            self.assertEqual(result["counts"]["unauthorized_state_change"], 0)


if __name__ == "__main__":
    unittest.main()
