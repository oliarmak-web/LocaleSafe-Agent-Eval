import json
from pathlib import Path
import unittest
from experiments.build_hindi_pair import build
from localesafe.handoff_eval import permission_record
from localesafe.operation_probe import jobs_for,messages_for,score


class OperationProbeTests(unittest.TestCase):
    def test_frozen_balance_and_hidden_labels(self):
        cases,_=build();jobs=jobs_for(cases)
        self.assertEqual(336,len(jobs))
        self.assertEqual(cases,json.loads(Path('experiments/operation-probe/cases.json').read_text(encoding='utf-8')))
        self.assertEqual(jobs,json.loads(Path('experiments/operation-probe/jobs.json').read_text(encoding='utf-8')))
        for case in cases:
            group=[j for j in jobs if j['case_id']==case['id']]
            expected=permission_record(case)['requested_action']['tool']
            positions=['ABC'[j['order'].index(expected)] for j in group]
            self.assertEqual([2,2,2],[positions.count(p) for p in 'ABC'])
            for j,letter in zip(group,positions):
                payload=json.loads(messages_for(case,j)[1]['content'])
                for event in payload['history']:
                    self.assertNotIn('permission',event);self.assertNotIn('requested_action',event)
                self.assertTrue(score(case,j,letter)['correct'])
                self.assertFalse(score(case,j,'"'+letter+'"')['valid_letter'])
                self.assertFalse(score(case,j,letter+' because')['valid_letter'])


if __name__=='__main__':unittest.main()
