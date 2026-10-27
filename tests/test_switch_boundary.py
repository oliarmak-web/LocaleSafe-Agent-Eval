import json
from pathlib import Path
import unittest

from experiments.build_switch_boundary import build, LAYOUTS
from localesafe.collect_switch_boundary import ordered_jobs
from localesafe.handoff_eval import permission_record
from localesafe.handoff_study import messages_for, score


class SwitchBoundaryTests(unittest.TestCase):
    def test_frozen_grid_dependencies_and_scope(self):
        cases, design=build()
        self.assertEqual(72,len(cases))
        self.assertEqual(cases,[json.loads(s) for s in Path('experiments/switch-boundary/cases.jsonl').read_text(encoding='utf-8').splitlines()])
        self.assertEqual(design,json.loads(Path('experiments/switch-boundary/design.json').read_text(encoding='utf-8')))
        jobs=ordered_jobs(cases,['greedy','sample-1','sample-2'],20261022)
        self.assertEqual(864,len(jobs))
        self.assertEqual({'summary','actor'},{j['stage'] for j in jobs})
        anchors={c['scenario']:c for c in cases if c['language_pattern']=='en-en'}
        for c in cases:
            self.assertEqual(4,len(c['events']))
            self.assertEqual(LAYOUTS[c['language_pattern']],tuple(e['language'] for e in c['events']))
            self.assertEqual(permission_record(anchors[c['scenario']]),permission_record(c))
            for old,neutral in ((c['events'][0],c['events'][1]),(c['events'][2],c['events'][3])):
                self.assertEqual(old['permission'],neutral['permission'])
                self.assertEqual(old['requested_action']['tool'],neutral['requested_action']['tool'])
            job=next(j for j in jobs if j['case_id']==c['id'] and j['stage']=='actor' and j['condition']=='oracle_record')
            anchor_job={**job,'case_id':anchors[c['scenario']]['id']}
            self.assertEqual(messages_for(c,job,{}),messages_for(anchors[c['scenario']],anchor_job,{}))
            self.assertTrue(score(c,job,json.dumps(permission_record(c)['requested_action']))['correct'])


if __name__=='__main__':unittest.main()
