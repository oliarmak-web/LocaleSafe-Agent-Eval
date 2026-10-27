import json
import unittest
from pathlib import Path

from experiments.build_handoff_study import build as original_build
from experiments.build_hindi_pair import build, PATTERNS
from localesafe.handoff_study import jobs_for, messages_for, score
from localesafe.handoff_eval import permission_record


class HindiPairTests(unittest.TestCase):
    def test_frozen_grid_and_original_preservation(self):
        cases, design = build()
        self.assertEqual(56, len(cases))
        self.assertEqual(1680, len(jobs_for(cases)))
        self.assertEqual(set(PATTERNS), {c['language_pattern'] for c in cases})
        frozen = [json.loads(line) for line in Path('experiments/hindi-pair/cases.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual(cases, frozen)
        self.assertEqual(design, json.loads(Path('experiments/hindi-pair/design.json').read_text(encoding='utf-8')))
        old, old_design = original_build()
        self.assertEqual([c for c in old if old_design[c['id']]['split']=='development'], cases[:32])

    def test_matched_semantics_and_hidden_labels(self):
        cases, _ = build()
        anchors = {c['scenario']: c for c in cases if c['language_pattern']=='en-en'}
        for case in cases:
            self.assertEqual(permission_record(anchors[case['scenario']]), permission_record(case))
            job = next(j for j in jobs_for([case], ['greedy']) if j['stage']=='actor' and j['condition']=='full_history')
            payload = json.loads(messages_for(case, job, {})[1]['content'])
            for event in payload['history']:
                self.assertNotIn('permission', event)
                self.assertNotIn('requested_action', event)
            result = score(case, job, json.dumps(permission_record(case)['requested_action']))
            self.assertTrue(result['correct'])


if __name__ == '__main__':
    unittest.main()
