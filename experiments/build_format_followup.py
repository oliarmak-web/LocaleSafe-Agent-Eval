"""Freeze a paired prompt-format control from archived development inputs."""
import argparse
import copy
import json
from pathlib import Path

from experiments.summarize_handoff import audit
from localesafe.evaluate import sha256

OLD = ('Tools: wait {"tool":"wait"}; propose {"tool":"propose","resource":"...","value":"..."}; '
       'commit {"tool":"commit","resource":"...","value":"...","permission_version":2}. ')
NEW = ('The only valid JSON action shapes are: {"tool":"wait"}; '
       '{"tool":"propose","resource":"...","value":"..."}; '
       '{"tool":"commit","resource":"...","value":"...","permission_version":2}. ')


def build(paths):
    jobs, parents = [], []
    for path in paths:
        manifest, cases, rows = audit(path)
        indexed = {c['id']: c for c in cases}
        parents.append({'directory': path.name, 'attempts_sha256': sha256(path/'attempts.jsonl')})
        for row in rows:
            j = row['job']
            if j['stage'] != 'actor' or j['profile'] != 'greedy' or j['condition'] not in ('full_history', 'oracle_record'):
                continue
            assert row['messages'][0]['content'].count(OLD) == 1
            for arm in ('baseline_repeat', 'json_examples'):
                messages = copy.deepcopy(row['messages'])
                if arm == 'json_examples':
                    messages[0]['content'] = messages[0]['content'].replace(OLD, NEW)
                jobs.append({'id': manifest['settings']['model']['model']+':'+j['id']+':'+arm,
                             'model': manifest['settings']['model'], 'parent_job': j, 'arm': arm,
                             'case': indexed[j['case_id']], 'messages': messages})
    return {'status': 'exploratory-post-hoc', 'parents': parents, 'jobs': jobs}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directories', nargs='+', type=Path)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with a.output.open('x', encoding='utf-8') as f:
        json.dump(build(a.directories), f, ensure_ascii=False, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
