import random
import unittest
from pathlib import Path

from localesafe.attribution_probe import assess, completed_jobs, paired_seed, prompt_for, validate_tasks
from localesafe.evaluate import read_jsonl
from localesafe.service_eval import date_context

ROOT = Path(__file__).resolve().parents[1]


class AttributionTests(unittest.TestCase):
    def setUp(self):
        self.tasks = read_jsonl(ROOT / "experiments/attribution/tasks.jsonl")

    def test_canonical_choices_validate_executor(self):
        validate_tasks(self.tasks)
        for task in self.tasks:
            if task["kind"] == "interpretation":
                correct = task["options"].index(date_context(task["case"])[0])
                self.assertTrue(assess(task, correct)["passed"])
            else:
                self.assertEqual(sum(assess(task, i)["passed"] for i in range(3)), 1)

    def test_labels_permute_without_gold_in_prompt(self):
        task = self.tasks[0]
        text = prompt_for(task, (2, 0, 1))[1]["content"]
        self.assertIn("A: ask for date clarification", text)
        self.assertNotIn("correct answer", text)
        self.assertNotIn("user_approves", text)

    def test_language_and_phrasing_share_sampling_uniform(self):
        same = [t for t in self.tasks if t["kind"] == "interpretation" and t["case"]["family"] == "march-april" and t["case"]["locale"] == "US"]
        self.assertEqual(len({paired_seed(t, (0, 1, 2), 0, 42) for t in same}), 1)

    def test_wrong_interpretation_is_not_executor_failure(self):
        task = self.tasks[0]
        score = assess(task, 1)
        self.assertFalse(score["context"])
        self.assertTrue(score["tools"])
        self.assertFalse(score["completion"])

    def test_resume_preserves_complete_groups_and_rejects_tampering(self):
        task, order = self.tasks[0], (0, 1, 2)
        rows = []
        for draw in range(3):
            seed = paired_seed(task, order, draw, 42)
            label = random.Random(seed).choices(range(3), weights=[1/3]*3, k=1)[0]
            rows.append({"id": task["case"]["id"], "order": list(order), "draw": draw,
                         "seed": seed, "probabilities_ABC": [1/3]*3, "chosen_label": "ABC"[label],
                         "selected_option": order[label], "messages": prompt_for(task, order),
                         "score": assess(task, order[label])})
        self.assertEqual(completed_jobs(rows, self.tasks, 3, 42), {(task["case"]["id"], order)})
        for invalid in (rows[:-1], rows + [rows[0]]):
            with self.assertRaises(ValueError):
                completed_jobs(invalid, self.tasks, 3, 42)
        rows[0]["score"] = {}
        with self.assertRaisesRegex(ValueError, "validation"):
            completed_jobs(rows, self.tasks, 3, 42)
