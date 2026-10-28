import json
from pathlib import Path
import unittest
from experiments.summarize_domain_study import audit,summarize,render
from experiments.summarize_domain_comparison import analyze,render as render_comparison
from localesafe.collect_domain_study import SOURCES
from localesafe.collect_domain_replication import EXTRA_SOURCES
from localesafe.collect_handoff import MODELS


class DomainArchiveTests(unittest.TestCase):
    def test_both_real_runs_and_reports(self):
        for label,model in [('qwen','qwen3-4b'),('phi','phi4-mini')]:
            path=Path('experiments/results')/f'domain-study-{model}-20261027'
            kwargs={} if label=='qwen' else {'model_specs':[MODELS[model]],'source_names':(*SOURCES,*EXTRA_SOURCES)}
            m,c,r=audit(path,**kwargs);result=summarize(m,c,r)
            self.assertEqual(result,json.loads(Path(f'experiments/analysis/domain-study/{label}.json').read_text(encoding='utf-8')))
            self.assertEqual(render(result),Path(f'docs/DOMAIN_{label.upper()}_RESULTS.md').read_text(encoding='utf-8'))
            self.assertEqual(720,len(r))
            self.assertEqual(4 if label=='qwen' else 0,sum(s['passed'] for s in result['english_screens']))
        result=analyze(Path('experiments/results/domain-study-qwen3-4b-20261027'),Path('experiments/results/domain-study-phi4-mini-20261027'))
        self.assertEqual(result,json.loads(Path('experiments/analysis/domain-study/comparison.json').read_text(encoding='utf-8')))
        self.assertEqual(render_comparison(result),Path('docs/DOMAIN_COMPARISON.md').read_text(encoding='utf-8'))


if __name__=='__main__':unittest.main()
