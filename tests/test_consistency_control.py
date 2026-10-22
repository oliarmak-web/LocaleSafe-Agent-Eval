import copy
import json
import unittest
from pathlib import Path

from experiments.consistency_control import analyze, compare, render


def row(language, repeat, correct):
    return {"scenario": "one", "condition": "baseline", "language": language,
            "repeat": repeat, "scores": {"strict": {"correct_action": correct}}}


class ConsistencyControlTests(unittest.TestCase):
    def test_same_total_success_can_hide_different_items(self):
        rows = [row("en", 0, True), row("en", 1, False),
                row("es", 0, False), row("es", 1, True)]
        original = copy.deepcopy(rows)
        result = compare(rows, "baseline")
        self.assertEqual(result["english_rerun"]["left_correct"], 1)
        self.assertEqual(result["english_rerun"]["left_only"], 1)
        self.assertEqual(result["same_repeat_target"]["es"]["left_only"], 1)
        self.assertEqual(result["other_repeat_target"]["es"]["left_only"], 0)
        self.assertEqual(rows, original)

    def test_zero_english_floor_is_not_missing_data(self):
        rows = [row(lang, repeat, False) for lang in ("en", "es") for repeat in (0, 1)]
        result = compare(rows, "baseline")
        self.assertEqual(result["english_rerun"]["left_correct"], 0)
        self.assertEqual(result["same_repeat_target"]["es"]["both_wrong"], 2)

    def test_missing_or_duplicate_attempt_is_rejected(self):
        rows = [row(lang, repeat, True) for lang in ("en", "es") for repeat in (0, 1)]
        for invalid in (rows[:-1], rows + [rows[0]], rows + [row("en", 2, True)]):
            with self.assertRaises(ValueError):
                compare(invalid, "baseline")

    def test_saved_analysis_and_report_match_audited_archives(self):
        root = Path(__file__).resolve().parents[1]
        result = analyze([root / "experiments" / "results" / f"workflow-gpu-qwen3-{size}-20261022" for size in ("06b", "17b")])
        saved = json.loads((root / "experiments" / "analysis" / "consistency-control.json").read_text(encoding="utf-8"))
        self.assertEqual(result, saved)
        self.assertEqual(render(result), (root / "docs" / "CONSISTENCY_CONTROL.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
