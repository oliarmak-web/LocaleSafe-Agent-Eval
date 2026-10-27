import json
import unittest
from localesafe.domain_study import cases,expected_action
from localesafe.domain_eval import evaluate


class DomainEvalTests(unittest.TestCase):
    def test_reference_partial_coverage_and_unsafe_change(self):
        data=cases()
        traces=[{'case_id':c['id'],'raw_output':json.dumps(expected_action(c))} for c in data]
        result=evaluate(data,traces,'synthetic')
        self.assertEqual(180,result['counts']['correct']);self.assertEqual(0,result['counts']['unauthorized_attempt'])
        partial=evaluate(data,traces[:1],'model')
        self.assertEqual(179,partial['missing']);self.assertEqual(1,partial['counts']['correct'])
        c=next(c for c in data if c['id']=='telecom:reversal:en')
        bad=[{'case_id':c['id'],'raw_output':'{"operation":"execute","target":"SERVICE-1","value":"cancelled"}'}]
        self.assertEqual(1,evaluate([c],bad,'synthetic')['counts']['guard_blocked'])
        with self.assertRaises(ValueError):evaluate(data,traces+traces[:1],'model')


if __name__=='__main__':unittest.main()
