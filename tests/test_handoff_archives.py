import json
import unittest
from pathlib import Path

from experiments.build_handoff_study import build
from experiments.build_monitor_followup import build as build_followup, RULES
from experiments.summarize_handoff import audit, summarize, render
from experiments.replay_handoff_routing import replay
from localesafe.collect_monitor_followup import score
from experiments.summarize_monitor_followup import audit as followup_audit, summarize as followup_summary, render as followup_render

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

    def test_analysis_matches_archives(self):
        summaries=[summarize(*audit(path)) for path in ARCHIVES]
        saved=json.loads((ROOT/'experiments/analysis/handoff/summary.json').read_text(encoding='utf-8'))
        self.assertEqual(summaries,saved)
        self.assertEqual(render(summaries),(ROOT/'docs/HANDOFF_RESULTS.md').read_text(encoding='utf-8'))
        routing=json.loads((ROOT/'experiments/analysis/handoff/routing.json').read_text(encoding='utf-8'))
        self.assertEqual([replay(path) for path in ARCHIVES],routing)

    def test_followup_archive_analysis_and_baseline_repeat(self):
        path=ROOT/'experiments/results/monitor-followup-qwen3-4b-20261022'
        manifest,plan,rows=followup_audit(path)
        self.assertEqual(len(rows),384)
        result=followup_summary(manifest,plan,rows)
        self.assertEqual(result,json.loads((ROOT/'experiments/analysis/handoff/monitor-followup.json').read_text(encoding='utf-8')))
        self.assertEqual(followup_render(result),(ROOT/'docs/MONITOR_FOLLOWUP.md').read_text(encoding='utf-8'))
        original={}
        for archive in ARCHIVES[:2]:
            _,_,prior=audit(archive)
            name=archive.name.removesuffix('-20261022')
            original.update({(name,r['job']['id']):r for r in prior})
        jobs={j['id']:j for j in plan['jobs']}
        for row in rows:
            job=jobs[row['job_id']]
            if job['condition']=='baseline_repeat':
                prior=original[job['parent'],job['parent_job_id']]
                self.assertEqual(row['messages'],prior['messages'])
                self.assertEqual(json.loads(row['raw_output']),json.loads(prior['raw_output']))


if __name__=='__main__':
    unittest.main()
