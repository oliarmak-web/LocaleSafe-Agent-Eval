import json
import unittest
from pathlib import Path

from experiments.summarize_handoff import audit, summarize, render


ROOT = Path(__file__).resolve().parents[1]


class ModelExtensionTests(unittest.TestCase):
    def test_complete_archives_reproduce_report_and_failed_gates(self):
        summaries = []
        for name, expected in [('mistral-7b-v03', (0, 1)), ('phi4-mini', (4, 8))]:
            path = ROOT / 'experiments/results' / f'handoff-{name}-development-20261022'
            manifest, cases, rows = audit(path)
            result = summarize(manifest, cases, rows)
            self.assertEqual(len(rows), 960)
            self.assertFalse(result['qualified_for_evaluation'])
            self.assertEqual(tuple(result['english_gate'][k]['correct'] for k in
                                   ('full_history', 'oracle_record')), expected)
            self.assertFalse((path.parent / f'handoff-{name}-evaluation-20261022').exists())
            summaries.append(result)
        saved = json.loads((ROOT / 'experiments/analysis/handoff/model-extension.json').read_text(encoding='utf-8'))
        self.assertEqual(summaries, saved)
        self.assertEqual(render(summaries), (ROOT / 'docs/MODEL_EXTENSION_RESULTS.md').read_text(encoding='utf-8'))
