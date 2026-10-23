import copy
import json
import unittest
from pathlib import Path

from localesafe.evaluate import read_jsonl
from localesafe.sales_pilot import cases, jobs_for, messages_for, score, seed_for, unsupported, LANGUAGES, PROFILES
from localesafe.collect_sales_pilot import ordered_jobs


class SalesPilotTests(unittest.TestCase):
    def test_frozen_grid_and_language_matched_truth(self):
        root=Path(__file__).resolve().parents[1]
        data=cases()
        self.assertEqual(data,read_jsonl(root/'experiments/sales-pilot/cases.jsonl'))
        self.assertEqual(len(data),30)
        self.assertEqual(len(jobs_for(data)),360)
        for family in {c['family'] for c in data}:
            group=[c for c in data if c['family']==family]
            self.assertEqual({c['language'] for c in group},set(LANGUAGES))
            self.assertTrue(all(c['requirements']==group[0]['requirements'] for c in group))
            self.assertTrue(all(c['review_status']=='AI-authored-draft' for c in group))
        self.assertTrue(all(len(c['history'])==2 for c in data if c['family']=='corrected_region'))

    def test_no_reference_leak_and_identical_oracle_generated_inputs(self):
        for case in cases():
            extraction={'id':'x','profile':'greedy','stage':'extract'}
            history={'id':'x','profile':'greedy','stage':'qualify_history'}
            altered=copy.deepcopy(case)
            altered['requirements']['budget_usd']=1
            for job in (extraction,history):
                self.assertEqual(messages_for(case,job,{}),messages_for(altered,job,{}))
            oracle={'id':'x','profile':'greedy','stage':'qualify_oracle'}
            generated={'id':'x','profile':'greedy','stage':'qualify_generated'}
            previous={case['id']+':greedy:extract':{'raw_output':json.dumps(case['requirements'])}}
            self.assertEqual(messages_for(case,oracle,{}),messages_for(case,generated,previous))
            previous[case['id']+':greedy:extract']['raw_output']='```invalid```'
            self.assertIn('requirements_text',json.loads(messages_for(case,generated,previous)[1]['content']))

    def test_exact_scoring_format_and_unsupported_claims(self):
        for case in cases():
            extraction={'stage':'extract'}
            self.assertTrue(score(case,extraction,json.dumps(case['requirements']))['correct'])
            self.assertFalse(score(case,extraction,'```json\n'+json.dumps(case['requirements'])+'\n```')['parsed'])
            bad=dict(case['requirements'],employees=True)
            self.assertFalse(score(case,extraction,json.dumps(bad))['parsed'])
            fields=unsupported(case['requirements'])
            good={'decision':'escalate' if fields else 'fit','unsupported':fields}
            self.assertTrue(score(case,{'stage':'qualify_history'},json.dumps(good))['correct'])
            false_fit=score(case,{'stage':'qualify_history'},'{"decision":"fit","unsupported":[]}')
            self.assertEqual(false_fit['unsupported_fit_claim'],bool(fields))

    def test_stage_dependencies_and_seed_blocks(self):
        data=cases()
        schedule=ordered_jobs(data,PROFILES,20261023)
        indices={j['id']:i for i,j in enumerate(schedule)}
        for job in schedule:
            if job['stage']=='qualify_generated':
                self.assertLess(indices[job['case_id']+':'+job['profile']+':extract'],indices[job['id']])
        group=[c for c in data if c['family']=='supported']
        for profile in PROFILES:
            self.assertEqual(len({seed_for(c,{'stage':'qualify_history','profile':profile}) for c in group}),1)
            self.assertEqual(seed_for(group[0],{'stage':'qualify_oracle','profile':profile}),
                             seed_for(group[0],{'stage':'qualify_generated','profile':profile}))
