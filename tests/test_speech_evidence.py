import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
import wave
from localesafe.speech_evidence import validate


class SpeechEvidenceTests(unittest.TestCase):
    def test_provenance_hash_review_and_path_checks(self):
        # Silence is a technical file-validation fixture, not a speech experiment.
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=root/'silence.wav'
            with wave.open(str(path),'wb') as w:
                w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000);w.writeframes(b'\0'*3200)
            event={'event_seq':1,'transcript':'technical test placeholder','audio_file':'silence.wav',
                   'audio_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'audio_origin':'synthetic',
                   'license':'CC0-1.0','consent':'synthetic_no_person'}
            row={'id':'technical-fixture','case_id':'security:domain_fact:en','source_kind':'asr_output',
                 'provider':'test-fixture-no-real-provider','provider_version':'test','settings':{},
                 'review_status':'unreviewed','reviewer_id':None,'events':[event]}
            manifest={'format_version':1,'records':[row]}
            self.assertEqual(1,validate(manifest,root)['records'])
            bad=copy.deepcopy(manifest);bad['records'][0]['events'][0]['audio_file']='../silence.wav'
            with self.assertRaisesRegex(ValueError,'Unsafe/missing'):validate(bad,root)
            bad=copy.deepcopy(manifest);bad['records'][0]['events'][0]['audio_sha256']='0'*64
            with self.assertRaisesRegex(ValueError,'hash mismatch'):validate(bad,root)
            bad=copy.deepcopy(manifest);bad['records'][0]['review_status']='independently-reviewed'
            with self.assertRaisesRegex(ValueError,'attribution'):validate(bad,root)
            bad=copy.deepcopy(manifest);bad['records'][0]['source_kind']='injected_text_control'
            with self.assertRaisesRegex(ValueError,'not audio evidence'):validate(bad,root)


if __name__=='__main__':unittest.main()
