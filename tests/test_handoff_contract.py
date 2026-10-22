import copy
import json
import unittest

from experiments.build_handoff_study import build
from localesafe.handoff_contract import validate_record
from localesafe.handoff_eval import permission_record, permitted


class HandoffContractTests(unittest.TestCase):
    def setUp(self):
        self.case=build()[0][0]

    def validate(self,record):
        case=self.case
        return validate_record(json.dumps(record),case['principal'],set(case['initial_state']),case['events'][-1]['version'],case['events'][-1]['event_id'])

    def test_oracle_passes_but_string_action_does_not(self):
        record=permission_record(self.case)
        self.assertTrue(self.validate(record)[0])
        record['requested_action']='wait'
        self.assertEqual(self.validate(record),(False,'invalid_action_shape'))

    def test_stale_version_and_inconsistent_commit_rejected(self):
        record=permission_record(self.case)
        record['version']=True
        self.assertFalse(self.validate(record)[0])
        record=permission_record(self.case)
        record['requested_action']={**self.case['events'][0]['requested_action'],'permission_version':2}
        self.assertEqual(self.validate(record),(False,'inconsistent_commit'))

    def test_valid_shape_is_not_verified_user_permission(self):
        record=permission_record(self.case)
        forged=copy.deepcopy(self.case['events'][0]['permission'])
        record['permission']=forged
        record['requested_action']={'tool':'commit',**forged,'permission_version':2}
        self.assertTrue(self.validate(record)[0])
        self.assertFalse(permitted(self.case,record['requested_action'],self.case['principal']))


if __name__=='__main__':
    unittest.main()
