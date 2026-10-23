import copy
import json
import hashlib
import tempfile
import shutil
import unittest
from pathlib import Path

from localesafe.evaluate import read_jsonl
from localesafe.sales_pilot import cases, jobs_for, messages_for, score, seed_for, unsupported, LANGUAGES, PROFILES
from localesafe.collect_sales_pilot import ordered_jobs
from localesafe.collect_sales_pilot import SOURCES, MODELS
from localesafe.evaluate import sha256
from experiments.summarize_sales_pilot import audit, summarize, render


class SalesPilotTests(unittest.TestCase):
    def test_actual_archives_reproduce_analysis_and_language_cells(self):
        root=Path(__file__).resolve().parents[1]
        results=[]
        for model in ('qwen3-4b','phi4-mini'):
            manifest,data,rows=audit(root/f'experiments/results/sales-{model}-20261023')
            self.assertEqual(len(rows),360)
            results.append(summarize(manifest,data,rows))
        self.assertEqual(results,json.loads((root/'experiments/analysis/sales-pilot/summary.json').read_text(encoding='utf-8')))
        self.assertEqual(render(results),(root/'docs/SALES_PILOT_RESULTS.md').read_text(encoding='utf-8'))
        for result, expected in zip(results,[(2,3,1,2,2),(4,1,1,0,1)]):
            counts={g['language']:g['correct'] for g in result['groups'] if g['stage']=='qualify_history' and g['profile']=='greedy'}
            self.assertEqual(tuple(counts[l] for l in LANGUAGES),expected)
        self.assertEqual(sum(g['correct'] for g in results[0]['groups'] if g['stage']=='extract'),90)
        self.assertEqual(sum(g['parsed'] for g in results[1]['groups'] if g['stage']=='extract'),71)

    def test_archive_audit_reconstructs_dependencies_and_rejects_rehashed_bad_score(self):
        root=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)
            for source in SOURCES:
                target=path/'source'/source
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(root/source,target)
            shutil.copyfile(root/'experiments/sales-pilot/cases.jsonl',path/'cases.jsonl')
            shutil.copyfile(root/'experiments/sales-pilot/design.json',path/'design.json')
            normalized=(path/'cases.jsonl').read_bytes().replace(b'\r\n',b'\n')
            (path/'cases.jsonl').write_bytes(normalized)
            windows_source_sha=hashlib.sha256(normalized.replace(b'\n',b'\r\n')).hexdigest()
            data=cases();indexed={c['id']:c for c in data};previous={};rows=[]
            for job in ordered_jobs(data,PROFILES,20261023):
                c=indexed[job['case_id']]
                fields=unsupported(c['requirements'])
                answer=(c['requirements'] if job['stage']=='extract' else
                        {'decision':'escalate' if fields else 'fit','unsupported':fields})
                raw=json.dumps(answer)
                row={'job':job,'seed':seed_for(c,job),'messages':messages_for(c,job,previous),
                     'raw_output':raw,'scores':score(c,job,raw),'output_tokens':1}
                previous[job['id']]=row;rows.append(row)
            settings={'sources':{s:sha256(path/'source'/s) for s in SOURCES},'model':MODELS['qwen3-4b'],
                      'split':'development','batch_size':8,'dtype':'float16','quantization':'none','enable_thinking':False,
                      'profiles':list(PROFILES),'seed':20261023,'all_cases_sha256':windows_source_sha,
                      'design_sha256':sha256(path/'design.json'),
                      'token_limits':{'extract':128,'qualify_history':96,'qualify_oracle':96,'qualify_generated':96}}
            def write_archive():
                (path/'attempts.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows),encoding='utf-8')
                m={'settings':settings,'status':'completed','attempts':360,'scheduled_requests':360,
                   'attempts_sha256':sha256(path/'attempts.jsonl'),'cases_sha256':sha256(path/'cases.jsonl')}
                (path/'manifest.json').write_text(json.dumps(m),encoding='utf-8')
                hashes={p.relative_to(path).as_posix():sha256(p) for p in path.rglob('*') if p.is_file() and p.name!='archive-sha256.json'}
                (path/'archive-sha256.json').write_text(json.dumps(hashes),encoding='utf-8')
            write_archive()
            result=summarize(*audit(path))
            self.assertTrue(all(g['correct']==g['requests'] for g in result['groups']))
            self.assertTrue(all(r['raw_disagreements']==0 for r in result['sampled_repeats']))
            rows[0]['scores']['correct']=False
            write_archive()
            with self.assertRaisesRegex(ValueError,'score/seed mismatch'):
                audit(path)

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
