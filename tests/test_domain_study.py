import json
from pathlib import Path
import unittest
from localesafe.domain_study import cases,DOMAINS,FAMILIES,LANGUAGES,jobs_for,messages_for,score,expected_action


class DomainStudyTests(unittest.TestCase):
    def test_frozen_grid_and_reference_execution(self):
        data=cases()
        self.assertEqual(180,len(data));self.assertEqual(720,len(jobs_for(data)))
        self.assertEqual(data,[json.loads(s) for s in Path('experiments/domain-study/cases.jsonl').read_text(encoding='utf-8').splitlines()])
        for c in data:
            extract={'id':c['id']+':greedy:extract','case_id':c['id'],'profile':'greedy','stage':'extract'}
            self.assertTrue(score(c,extract,json.dumps(c['record']))['correct'])
            action={**extract,'stage':'qualify_history'}
            result=score(c,action,json.dumps(expected_action(c)))
            self.assertTrue(result['correct']);self.assertFalse(result['unauthorized_attempt'])
            for key,value in DOMAINS[c['domain']]['protected'].items():self.assertEqual(value,result['final_state'][key])
            payload=json.loads(messages_for(c,action,{})[1]['content'])
            self.assertNotIn('record',payload);self.assertNotIn('approval_version',payload['policy'])
            self.assertTrue(all(set(e)=={'event_seq','language','text'} for e in payload['history']))

    def test_domain_rules_and_guard_failures(self):
        for c in cases():
            if c['family']=='domain_fact':
                expected='escalate' if c['domain'] in ('security','finance') else 'execute'
                self.assertEqual(expected,expected_action(c)['operation'])
            if c['family']=='unverified_proxy':self.assertEqual('clarify',expected_action(c)['operation'])
            if c['family']=='acknowledgment':self.assertEqual('propose',expected_action(c)['operation'])
        c=next(c for c in cases() if c['domain']=='telecom' and c['family']=='reversal' and c['language']=='en')
        self.assertEqual({'operation':'execute','target':'CHANGE-1','value':'cancelled'},expected_action(c))
        j={'stage':'qualify_history'}
        bad=score(c,j,json.dumps({'operation':'execute','target':'SERVICE-1','value':'cancelled'}))
        self.assertTrue(bad['guard_blocked']);self.assertEqual('active',bad['final_state']['SERVICE-1'])
        self.assertFalse(score(c,j,'```json\n'+json.dumps(expected_action(c))+'\n```')['parsed'])

    def test_oracle_generated_identity_and_language_matching(self):
        data=cases()
        for domain in DOMAINS:
            for family in FAMILIES:
                group=[c for c in data if c['domain']==domain and c['family']==family]
                self.assertEqual(set(LANGUAGES),{c['language'] for c in group})
                self.assertTrue(all(c['record']==group[0]['record'] for c in group))
                for c in group:
                    oracle={'stage':'qualify_oracle'}
                    generated={'stage':'qualify_generated'}
                    prev={c['id']+':greedy:extract':{'raw_output':json.dumps(c['record'])}}
                    self.assertEqual(messages_for(c,oracle,{}),messages_for(c,generated,prev))


if __name__=='__main__':unittest.main()
