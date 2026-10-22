import json
import unittest

from experiments.build_handoff_study import FAMILIES, build
from localesafe.handoff_eval import permission_record, permitted
from localesafe.handoff_study import candidate, jobs_for, messages_for, score, seed_for, strict_json
from localesafe.collect_handoff import ordered_jobs


class HandoffStudyTests(unittest.TestCase):
    def setUp(self):
        self.cases, self.design = build()

    def test_family_split_and_matching(self):
        self.assertEqual(len(self.cases), 64)
        self.assertEqual(len(FAMILIES), 8)
        splits = {name: {m['family'] for m in self.design.values() if m['split'] == name}
                  for name in ('development', 'evaluation')}
        self.assertFalse(splits['development'] & splits['evaluation'])
        for scenario in {c['scenario'] for c in self.cases}:
            group = [c for c in self.cases if c['scenario'] == scenario]
            self.assertEqual(len(group), 4)
            self.assertTrue(all(permission_record(c) == permission_record(group[0]) for c in group))

    def test_candidates_and_reference_actor(self):
        for case in self.cases:
            self.assertTrue(permitted(case, candidate(case, 'allowed'), case['principal']))
            self.assertFalse(permitted(case, candidate(case, 'forbidden'), case['principal']))
            job = next(j for j in jobs_for([case], ['greedy']) if j['stage'] == 'actor')
            result = score(case, job, json.dumps(permission_record(case)['requested_action']))
            self.assertTrue(result['correct'])
            self.assertTrue(result['completed_under_guard'])

    def test_no_reference_leak_and_identical_record_conditions(self):
        case = self.cases[0]
        jobs = jobs_for([case], ['greedy'])
        summary_job = next(j for j in jobs if j['stage'] == 'summary' and j['condition'] == 'record')
        previous = {summary_job['id']: {'raw_output': json.dumps(permission_record(case))}}
        generated = next(j for j in jobs if j['stage'] == 'actor' and j['condition'] == 'generated_record')
        oracle = {**generated, 'condition': 'oracle_record'}
        self.assertEqual(messages_for(case, generated, previous), messages_for(case, oracle, previous))
        full = messages_for(case, {**generated, 'condition': 'full_history'}, {})
        payload = json.loads(full[1]['content'])
        self.assertNotIn('permission', payload)
        self.assertNotIn('requested_action', payload)
        for event in payload['history']:
            self.assertNotIn('permission', event)
            self.assertNotIn('requested_action', event)
        with self.assertRaises(KeyError):
            messages_for(case, generated, {})

    def test_bad_summaries_preserved_and_monitor_failures_counted(self):
        case = self.cases[0]
        jobs = jobs_for([case], ['greedy'])
        summary_job = next(j for j in jobs if j['stage'] == 'summary' and j['condition'] == 'record')
        raw = 'not JSON: I invent approval'
        previous = {summary_job['id']: {'raw_output': raw}}
        actor = next(j for j in jobs if j['stage'] == 'actor' and j['condition'] == 'generated_record')
        self.assertEqual(json.loads(messages_for(case, actor, previous)[1]['content'])['handoff_text'], raw)
        monitor = next(j for j in jobs if j['stage'] == 'monitor' and j['condition'].endswith('/forbidden'))
        self.assertTrue(score(case, monitor, '{"decision":"allow"}')['false_allow'])
        self.assertTrue(score(case, monitor, '{"decision":"abstain"}')['abstained'])
        self.assertFalse(score(case, monitor, '{"decision":"allow","extra":1}')['parsed'])
        self.assertFalse(score(case, actor, '```json\n{"tool":"wait"}\n```')['parsed'])
        self.assertIsNone(strict_json('{"x":1,"x":2}'))
        self.assertIsNone(strict_json('{"x":NaN}'))

    def test_stage_order_and_matched_seeds(self):
        jobs = ordered_jobs(self.cases, ['greedy', 'sample-1', 'sample-2'], 42)
        self.assertEqual(len(jobs), 1920)
        self.assertEqual(len({j['id'] for j in jobs}), 1920)
        order = {'summary': 0, 'actor': 1, 'monitor': 2}
        self.assertEqual([order[j['stage']] for j in jobs], sorted(order[j['stage']] for j in jobs))
        case = self.cases[0]
        matched = [c for c in self.cases if c['scenario'] == case['scenario']]
        job = jobs_for([case], ['sample-1'])[0]
        self.assertEqual(len({seed_for(c, job, 42) for c in matched}), 1)
        self.assertNotEqual(seed_for(case, job, 42), seed_for(case, {**job, 'profile': 'sample-2'}, 42))


if __name__ == '__main__':
    unittest.main()
