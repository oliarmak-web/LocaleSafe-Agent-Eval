import json
import unittest
import tempfile
from pathlib import Path

from experiments.build_handoff_study import build as original_build
from experiments.build_hindi_pair import build, PATTERNS
from localesafe.handoff_study import jobs_for, messages_for, score
from localesafe.handoff_eval import permission_record
from localesafe.collect_handoff import MODELS, SOURCES, ordered_jobs
from localesafe.collect_hindi_pair import EXTRA_SOURCES
from localesafe.handoff_study import seed_for
from localesafe.evaluate import sha256
from experiments.summarize_hindi_pair import analyze, render


class HindiPairTests(unittest.TestCase):
    def test_frozen_grid_and_original_preservation(self):
        cases, design = build()
        self.assertEqual(56, len(cases))
        self.assertEqual(1680, len(jobs_for(cases)))
        self.assertEqual(set(PATTERNS), {c['language_pattern'] for c in cases})
        frozen = [json.loads(line) for line in Path('experiments/hindi-pair/cases.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual(cases, frozen)
        self.assertEqual(design, json.loads(Path('experiments/hindi-pair/design.json').read_text(encoding='utf-8')))
        old, old_design = original_build()
        self.assertEqual([c for c in old if old_design[c['id']]['split']=='development'], cases[:32])

    def test_matched_semantics_and_hidden_labels(self):
        cases, _ = build()
        anchors = {c['scenario']: c for c in cases if c['language_pattern']=='en-en'}
        for case in cases:
            self.assertEqual(permission_record(anchors[case['scenario']]), permission_record(case))
            job = next(j for j in jobs_for([case], ['greedy']) if j['stage']=='actor' and j['condition']=='full_history')
            payload = json.loads(messages_for(case, job, {})[1]['content'])
            for event in payload['history']:
                self.assertNotIn('permission', event)
                self.assertNotIn('requested_action', event)
            result = score(case, job, json.dumps(permission_record(case)['requested_action']))
            self.assertTrue(result['correct'])

    def test_auditor_recomputes_matched_losses_and_rejects_tampering(self):
        cases, design = build()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'cases.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in cases),encoding='utf-8')
            (root/'design.json').write_text(json.dumps(design),encoding='utf-8')
            sources = {}
            for name in (*SOURCES,*EXTRA_SOURCES):
                target=root/'source'/name
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(Path(name).read_bytes())
                sources[name]=sha256(target)
            settings={'model':MODELS['qwen3-4b'],'split':'development','profiles':['greedy','sample-1','sample-2'],
                      'seed':20261022,'dtype':'float16','quantization':'none','batch_size':8,'transformers':'4.57.6',
                      'gpu':'Tesla T4','enable_thinking':False,'token_limits':{'summary':192,'actor':96,'monitor':24},
                      'temperature':0.7,'top_p':0.8,'top_k':20,'sources':sources,
                      'all_cases_sha256':sha256(root/'cases.jsonl'),'design_sha256':sha256(root/'design.json')}
            indexed={c['id']:c for c in cases}
            previous={}
            rows=[]
            for job in ordered_jobs(cases,settings['profiles'],20261022):
                case=indexed[job['case_id']]
                if job['stage']=='summary':
                    raw=json.dumps(permission_record(case)) if job['condition']=='record' else 'Reference narrative'
                elif job['stage']=='actor':raw=json.dumps(permission_record(case)['requested_action'])
                else:raw=json.dumps({'decision':'allow' if job['condition'].endswith('/allowed') else 'block'})
                if (case['id']=='change_value-0-en-hi' and job['stage']=='actor'
                    and job['condition']=='full_history' and job['profile']=='greedy'):raw='{}'
                row={'job':job,'seed':seed_for(case,job,20261022),'messages':messages_for(case,job,previous),
                     'raw_output':raw,'output_tokens':1,'scores':score(case,job,raw)}
                previous[job['id']]=row
                rows.append(row)
            (root/'attempts.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
            manifest={'status':'completed','settings':settings,'attempts':1680,'scheduled_requests':1680,
                      'attempts_sha256':sha256(root/'attempts.jsonl'),'cases_sha256':sha256(root/'cases.jsonl')}
            (root/'manifest.json').write_text(json.dumps(manifest),encoding='utf-8')
            def rehash():
                hashes={p.relative_to(root).as_posix():sha256(p) for p in root.rglob('*')
                        if p.is_file() and p.name!='archive-sha256.json'}
                (root/'archive-sha256.json').write_text(json.dumps(hashes),encoding='utf-8')
            rehash()
            result=analyze(root)
            matched=next(c for c in result['matched_greedy_comparisons'] if c['switch']=='en-hi' and c['baseline']=='hi-hi')
            self.assertEqual(['change_value-0'],matched['losses'])
            self.assertEqual([],matched['gains'])
            self.assertIn('| en-hi | hi-hi | 1/8 | 0/8 |',render(result))
            rows[0]['scores']={'forged':True}
            (root/'attempts.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows),encoding='utf-8')
            manifest['attempts_sha256']=sha256(root/'attempts.jsonl')
            (root/'manifest.json').write_text(json.dumps(manifest),encoding='utf-8')
            rehash()
            with self.assertRaisesRegex(ValueError,'score/seed mismatch'):analyze(root)


if __name__ == '__main__':
    unittest.main()
