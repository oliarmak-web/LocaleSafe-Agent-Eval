import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from localesafe.evaluate import read_jsonl
from localesafe.service_eval import date_context, evaluate_service, replay

ROOT = Path(__file__).resolve().parents[1] / "examples/service"


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.cases = read_jsonl(ROOT / "cases.jsonl")
        self.traces = read_jsonl(ROOT / "oracle-traces.jsonl")
        self.pairs = read_jsonl(ROOT / "comparisons.jsonl")

    def test_oracle_replay_passes_every_language_and_context(self):
        report = evaluate_service(self.cases, self.traces, self.pairs)
        self.assertEqual(report["scores"]["passed"], {"correct": 11, "assessed": 11, "unknown_or_not_applicable": 0})

    def test_language_does_not_choose_date_convention(self):
        en, es, gb = self.cases[0], self.cases[1], self.cases[2]
        self.assertEqual(date_context(en), date_context(es))
        self.assertEqual(date_context(en)[0], "2027-03-04")
        self.assertEqual(date_context(gb)[0], "2027-04-03")

    def test_injected_faults_hit_different_layers(self):
        report = evaluate_service(self.cases, read_jsonl(ROOT / "faulty-traces.jsonl"), self.pairs)
        rows = {r["id"]: r for r in report["cases"]}
        self.assertFalse(rows["en-US"]["consent"])
        self.assertEqual(rows["en-US"]["events"][-1]["response"]["status"], "blocked_no_confirmation")
        self.assertTrue(rows["es-GB"]["tools"])  # Correct execution of a wrong interpreted date.
        self.assertFalse(rows["es-GB"]["context"])
        self.assertFalse(rows["es-GB"]["completion"])
        self.assertFalse(rows["en-unknown"]["clarification"])
        self.assertFalse(rows["es-handoff"]["handoff"])
        self.assertEqual(report["scores"]["passed"]["correct"], 7)

    def test_edit_revokes_confirmation_and_duplicates_are_blocked(self):
        trace = copy.deepcopy(self.traces[0])
        trace["actions"].insert(2, {"name": "draft_change", "arguments": {"appointment_id": "A1", "date": "2027-03-05"}})
        self.assertEqual(replay(self.cases[0], trace)["unauthorized_attempts"], 1)
        trace = copy.deepcopy(self.traces[0])
        trace["actions"].append({"name": "submit_change", "arguments": {}})
        result = replay(self.cases[0], trace)
        self.assertFalse(result["tools"])
        self.assertEqual(result["events"][-1]["response"]["status"], "blocked_duplicate")

    def test_consent_denial_is_a_valid_completed_outcome(self):
        row = next(c for c in self.cases if c["id"] == "en-deny")
        trace = next(t for t in self.traces if t["id"] == row["id"])
        result = replay(row, trace)
        self.assertTrue(result["passed"])
        self.assertIsNone(result["final_state"]["committed"])

    def test_invalid_traces_are_failed_not_fabricated_decisions(self):
        trace = dict(self.traces[0], actions=[{"name": "grant_myself_consent", "arguments": {}}])
        result = replay(self.cases[0], trace)
        self.assertFalse(result["format_valid"])
        self.assertIsNone(result["context"])
        self.assertFalse(result["passed"])

    def test_comparison_cannot_change_hidden_workflow_policy(self):
        cases = copy.deepcopy(self.cases)
        cases[1]["user_approves"] = False
        with self.assertRaisesRegex(ValueError, "uncontrolled"):
            evaluate_service(cases, self.traces, self.pairs)

    def test_missing_traces_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_service(self.cases, self.traces[:-1], self.pairs)

    def test_cli_records_origin_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            command = [sys.executable, "-m", "localesafe.service_eval", "--cases", str(ROOT / "cases.jsonl"),
                       "--traces", str(ROOT / "faulty-traces.jsonl"), "--comparisons", str(ROOT / "comparisons.jsonl"),
                       "--trace-origin", "synthetic", "--output", str(output)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = output.read_bytes()
            report = json.loads(original)
            self.assertEqual(report["trace_origin"], "synthetic")
            self.assertEqual(report["scores"]["passed"]["correct"], 7)
            self.assertEqual(report["by_locale"]["GB"]["context"]["correct"], 1)
            self.assertEqual(len(report["comparisons"]), 8)
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
            self.assertEqual(original, output.read_bytes())
