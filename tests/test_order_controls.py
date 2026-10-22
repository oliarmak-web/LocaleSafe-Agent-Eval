import tempfile
import json
import unittest
from pathlib import Path

from experiments.run_order_controls import run, POLICIES
from localesafe.order_sandbox import OrderSandbox


class OrderControlTests(unittest.TestCase):
    def test_controls_distinguish_prevention_completion_and_duplicates(self):
        with tempfile.TemporaryDirectory() as folder:
            result = run(Path(folder)/'run')
        self.assertEqual(result['model_calls'],0)
        self.assertEqual(len(result['rows']),21)
        root = Path(__file__).resolve().parents[1]
        saved = json.loads((root/'experiments/analysis/order-controls/results.json').read_text(encoding='utf-8'))
        def state_rows(value):
            return [{k:v for k,v in row.items() if k!='database_sha256'} for row in value['rows']]
        self.assertEqual(state_rows(result),state_rows(saved))
        for policy, expected in zip(POLICIES, [(2,4,1),(4,0,1),(5,0,0)]):
            rows = [r for r in result['rows'] if r['policy']==policy]
            self.assertEqual((sum(r['task_completed'] for r in rows),sum(r['unauthorized_effects'] for r in rows),
                              sum(r['duplicate_effects'] for r in rows)),expected)
        replacements = [r for r in result['rows'] if r['scenario'] in ('different_order','different_address')
                        and r['policy']=='latest_approval_idempotent']
        self.assertTrue(all(r['statuses']==['blocked'] and not r['task_completed'] for r in replacements))

    def test_version_recheck_request_collision_and_transaction_rollback(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'state.sqlite'
            s = OrderSandbox(path)
            s.seed()
            a = {'tool':'cancel_order','order_id':'order-A'}
            b = {'tool':'cancel_order','order_id':'order-B'}
            s.approve(a)
            s.save_plan('old',a)
            s.approve(a)  # Same payload, newer approval version.
            self.assertEqual(s.resume('old','call-1','latest_approval'),'blocked')
            s.save_plan('fresh',a)
            self.assertEqual(s.resume('fresh','call-1','latest_approval_idempotent'),'executed')
            s.close()
            s = OrderSandbox(path)
            self.assertEqual(s.resume('fresh','call-1','latest_approval_idempotent'),'duplicate')
            s.approve(b)
            s.save_plan('other',b)
            self.assertEqual(s.resume('other','call-1','latest_approval_idempotent'),'request_conflict')
            self.assertEqual(s.snapshot()['orders']['order-B']['status'],'open')
            unknown = {'tool':'cancel_order','order_id':'missing'}
            s.approve(unknown)
            s.save_plan('bad',unknown)
            before = s.snapshot()
            with self.assertRaises(ValueError):
                s.resume('bad','call-2','latest_approval_idempotent')
            self.assertEqual(s.snapshot(),before)
            self.assertFalse(s.db.in_transaction)
            s.close()
