import json
from pathlib import Path
import unittest
from experiments.build_hindi_pair import build
from localesafe.handoff_eval import permission_record
from localesafe.operation_probe import jobs_for,messages_for,score
from experiments.summarize_operation_probe import analyze,render


class OperationProbeTests(unittest.TestCase):
    def test_archived_results_and_order_effects(self):
        result=analyze(Path('experiments/results/operation-probe-qwen3-4b-20261027'),
                       Path('experiments/results/hindi-pair-qwen3-4b-20261027'))
        self.assertEqual(result,json.loads(Path('experiments/analysis/operation-probe/summary.json').read_text(encoding='utf-8')))
        self.assertEqual(render(result),Path('docs/OPERATION_PROBE_RESULTS.md').read_text(encoding='utf-8'))
        self.assertEqual(336,sum(r['valid'] for r in result['groups']))
        self.assertTrue(all(not r['all_orders_correct'] and len(r['order_sensitive_correctness'])==8 for r in result['groups']))
        self.assertEqual(0,sum(r['selected_letters'].get('A',0) for r in result['groups']))
        en=next(r for r in result['groups'] if r['pattern']=='en-en')
        self.assertEqual(24,en['correct'])
        self.assertEqual({'A':{'correct':0,'n':16},'B':{'correct':16,'n':16},'C':{'correct':8,'n':16}},en['accuracy_by_reference_letter'])

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
