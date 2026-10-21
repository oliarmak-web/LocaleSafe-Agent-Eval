import unittest
import tempfile

from pathlib import Path
from localesafe.evaluate import read_jsonl

def build():
    return read_jsonl(Path(__file__).resolve().parents[1] / "experiments/direct/cases.jsonl")
from experiments.summarize_direct import summarize
from localesafe.direct_probe import score_answer
from localesafe.service_eval import date_context


class DirectSummaryTests(unittest.TestCase):
    def test_new_fixtures_keep_reply_consistent_with_locale(self):
        from experiments.build_direct_cases import build as generate
        with tempfile.TemporaryDirectory() as directory:
            generate(Path(directory))
            records = read_jsonl(Path(directory) / "cases.jsonl")
        for record in records:
            case = record["case"]
            self.assertEqual(case["clarified_date"], date_context(case)[1])

    def test_script_repair_changes_outcome_without_changing_answer(self):
        record = next(r for r in build() if r["case"]["locale"] == "GB")
        flawed = {**record, "case": {**record["case"], "clarified_date": "2027-03-04"}}
        self.assertTrue(score_answer(flawed, "CLARIFY")["strict"]["wrong_commit"])
        fixed = {**flawed, "case": {**flawed["case"], "clarified_date": date_context(flawed["case"])[1]}}
        score = score_answer(fixed, "CLARIFY")["strict"]
        self.assertFalse(score["correct"])
        self.assertTrue(score["completed"])
        self.assertFalse(score["wrong_commit"])

    def test_clarification_can_recover_without_correct_interpretation(self):
        record = next(r for r in build() if r["date_kind"] == "iso")
        score = score_answer(record, "CLARIFY")["strict"]
        self.assertFalse(score["correct"])
        self.assertTrue(score["unnecessary_clarification"])
        self.assertTrue(score["completed"])
        self.assertFalse(score["wrong_commit"])

    def test_paired_counts_use_matched_items(self):
        rows = []
        for record in build():
            case = record["case"]
            selected = date_context(case)[0]
            raw = "CLARIFY" if selected == "ambiguous" else selected
            rows.append({**{k: case[k] for k in ("id", "family", "locale", "language")},
                         "date_kind": record["date_kind"], "repeat": 0,
                         "scores": score_answer(record, raw)})
        result = summarize(rows)["strict"]
        self.assertEqual(result["overall"]["correct"], 40)
        self.assertEqual(result["paired_with_english"]["uk"]["both_correct"], 8)
        self.assertEqual(result["language_date_kind"]["zh-Hans"]["iso"]["attempts"], 1)
