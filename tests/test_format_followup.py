import copy
import unittest
from pathlib import Path

from experiments.build_format_followup import build, OLD, NEW


class FormatFollowupTests(unittest.TestCase):
    def test_only_example_presentation_changes_and_all_pairs_are_present(self):
        root = Path(__file__).resolve().parents[1]
        paths = [root/'experiments/results'/f'handoff-{m}-development-20261022'
                 for m in ('mistral-7b-v03', 'phi4-mini')]
        plan = build(paths)
        self.assertEqual(len(plan['jobs']), 256)
        pairs = {}
        for job in plan['jobs']:
            key = (job['model']['model'], job['parent_job']['id'])
            pairs.setdefault(key, {})[job['arm']] = job
            self.assertNotIn('reference_allowed', job['messages'][1]['content'])
            self.assertNotIn('expected_action', job['messages'][1]['content'])
        self.assertEqual(len(pairs), 128)
        for group in pairs.values():
            baseline, changed = group['baseline_repeat'], group['json_examples']
            expected = copy.deepcopy(baseline['messages'])
            expected[0]['content'] = expected[0]['content'].replace(OLD, NEW)
            self.assertEqual(expected, changed['messages'])
            self.assertEqual(baseline['case'], changed['case'])
            self.assertEqual(baseline['parent_job'], changed['parent_job'])
