import unittest
from pathlib import Path

from localesafe.direct_probe import messages_for, parse_answer, score_answer
from localesafe.evaluate import read_jsonl
from localesafe.service_eval import date_context

ROOT = Path(__file__).resolve().parents[1]


class DirectProbeTests(unittest.TestCase):
    def setUp(self):
        self.records = read_jsonl(ROOT / "experiments/direct/cases.jsonl")

    def test_five_languages_same_design(self):
        self.assertEqual(len(self.records), 40)
        self.assertEqual({r["case"]["language"] for r in self.records}, {"en", "es", "zh-Hans", "uk", "ht"})
        for record in self.records:
            expected = date_context(record["case"])[0]
            raw = "CLARIFY" if expected == "ambiguous" else expected
            self.assertTrue(score_answer(record, raw)["strict"]["completed"])

    def test_no_locale_is_needed_for_iso_or_month_name(self):
        for record in self.records:
            if record["date_kind"] != "numeric":
                self.assertIsNone(record["case"]["locale"])
                self.assertNotEqual(date_context(record["case"])[0], "ambiguous")

    def test_strict_and_fence_diagnostic_stay_separate(self):
        self.assertIsNone(parse_answer('```text\n2027-03-04\n```'))
        self.assertEqual(parse_answer('```text\n2027-03-04\n```', True), "2027-03-04")
        for raw in ('The date is 2027-03-04.', '"2027-03-04"', '2027-13-04'):
            self.assertIsNone(parse_answer(raw, True))

    def test_wrong_interpretation_can_commit_wrong_date(self):
        record = next(r for r in self.records if r["case"]["id"] == "march-april-GB-en")
        score = score_answer(record, "2027-03-04")["strict"]
        self.assertFalse(score["correct"])
        self.assertTrue(score["wrong_commit"])
        self.assertTrue(score["sandbox"]["tools"])

    def test_hidden_script_not_in_prompt(self):
        record = dict(self.records[0], case=dict(self.records[0]["case"], clarified_date="2099-12-31"))
        prompt = str(messages_for(record))
        self.assertNotIn("2099-12-31", prompt)
        self.assertNotIn("A:", prompt)
