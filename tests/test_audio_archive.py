import json
from pathlib import Path
import unittest
from experiments.summarize_audio_smoke import audit,summarize,render


class AudioArchiveTests(unittest.TestCase):
    def test_real_transcripts_metrics_and_paired_features(self):
        m,s,r=audit(Path('experiments/results/audio-whisper-small-20261027'))
        result=summarize(m,s,r)
        self.assertEqual(result,json.loads(Path('experiments/analysis/audio-pilot/summary.json').read_text(encoding='utf-8')))
        self.assertEqual(render(result),Path('docs/AUDIO_SMOKE_RESULTS.md').read_text(encoding='utf-8'))
        self.assertEqual((20,40),(len(s),len(r)))
        self.assertTrue(all(p['identical_decoded_output'] and p['equal_edits'] for p in result['paired_language_hint']))
        self.assertTrue(all(g['posthoc_reference_basis']=='released_asr_hypothesis' for g in result['groups'] if g['dataset']=='PolyAI/minds14'))


if __name__=='__main__':unittest.main()
