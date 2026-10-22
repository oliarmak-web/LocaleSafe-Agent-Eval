import json
import unittest
from pathlib import Path

from experiments.build_handoff_study import build
from experiments.build_monitor_followup import build as build_followup, RULES
from experiments.summarize_handoff import audit, summarize
from localesafe.collect_monitor_followup import score

ROOT=Path(__file__).resolve().parents[1]
ARCHIVES=[ROOT/'experiments/results'/name for name in (
    'handoff-qwen3-4b-development-20261022', 'handoff-qwen3-4b-evaluation-20261022',
    'handoff-smollm3-3b-development-20261022')]


class HandoffArchiveTests(unittest.TestCase):
    def test_archives_are_complete_replayable_and_family_split(self):
        all_cases, design=build()
        for path in ARCHIVES:
            manifest,cases,rows=audit(path)
            self.assertEqual(len(rows),960)
            self.assertEqual(cases,[c for c in all_cases if design[c['id']]['split']==manifest['settings']['split']])
            result=summarize(manifest,cases,rows)
            expected=path.name.startswith('handoff-qwen3-4b-development')
            self.assertEqual(result['qualified_for_evaluation'],expected)

    def test_followup_has_exact_baseline_and_no_label_in_messages(self):
        paths=ARCHIVES[:2]
        # Directory names in the plan retain the original Colab source names.
        plan=json.loads((ROOT/'experiments/monitor-followup/jobs.json').read_text(encoding='utf-8'))
        recreated=build_followup(paths)
        def normalize(value):
            return json.loads(json.dumps(value).replace('-20261022',''))
        self.assertEqual(normalize(recreated),plan)
        self.assertEqual(len(plan['jobs']),384)
        by_key={}
        for job in plan['jobs']:
            by_key.setdefault(job['parent_job_id'],{})[job['condition']]=job
            self.assertNotIn('reference_allowed',job['messages'][1]['content'])
        for group in by_key.values():
            a,b=group['baseline_repeat'],group['explicit_rules']
            self.assertEqual(a['messages'][1],b['messages'][1])
            self.assertEqual(a['messages'][0]['content']+RULES,b['messages'][0]['content'])

    def test_monitor_abstention_and_invalid_are_not_correct(self):
        job={'reference_allowed':False}
        self.assertTrue(score(job,'{"decision":"allow"}')['false_allow'])
        self.assertTrue(score(job,'{"decision":"abstain"}')['abstained'])
        self.assertFalse(score(job,'{"decision":"abstain"}')['correct'])
        self.assertFalse(score(job,'{"decision":"allow","decision":"block"}')['parsed'])


if __name__=='__main__':
    unittest.main()
