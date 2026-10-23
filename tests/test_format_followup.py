import copy
import json
import unittest
from pathlib import Path

from experiments.build_format_followup import build, OLD, NEW
from experiments.summarize_format_followup import audit, summarize
from localesafe.evaluate import read_jsonl


class FormatFollowupTests(unittest.TestCase):
    def test_mistral_archive_replays_scores_and_exact_baseline(self):
        root = Path(__file__).resolve().parents[1]
        path = root/'experiments/results/format-mistral-7b-v03-20261022'
        manifest, jobs, rows = audit(path)
        frozen = json.loads((root/'experiments/format-followup/jobs.json').read_text(encoding='utf-8'))
        self.assertEqual(json.loads((path/'jobs.json').read_text(encoding='utf-8')), frozen)
        original = read_jsonl(root/'experiments/results/handoff-mistral-7b-v03-development-20261022/attempts.jsonl')
        result = summarize(manifest,jobs,rows,original)
        self.assertEqual(result,json.loads((root/'experiments/analysis/format-followup/mistral.json').read_text(encoding='utf-8'))[0])
        self.assertEqual(result['baseline_replay']['exact_text_agreement'],64)
        self.assertEqual([(g['parsed'],g['correct']) for g in result['groups']],[(0,0),(32,32),(12,4),(32,16)])
        self.assertEqual(result['paired'],{'helped':44,'hurt':0})

    def test_only_example_presentation_changes_and_all_pairs_are_present(self):
        root = Path(__file__).resolve().parents[1]
        paths = [root/'experiments/results'/f'handoff-{m}-development-20261022'
                 for m in ('mistral-7b-v03', 'phi4-mini')]
        plan = build(paths)
        self.assertEqual(plan, json.loads((root/'experiments/format-followup/jobs.json').read_text(encoding='utf-8')))
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
