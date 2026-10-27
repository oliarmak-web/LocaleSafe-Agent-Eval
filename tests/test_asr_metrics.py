import unittest
from localesafe.asr_metrics import edit_distance,normalize,score


class ASRMetricTests(unittest.TestCase):
    def test_true_levenshtein_and_unicode_normalization(self):
        self.assertEqual(3,edit_distance('kitten','sitting'))
        self.assertEqual(1,edit_distance('abc','axc'))
        self.assertTrue(score('Hello, WORLD!','hello world')['normalized_exact'])
        self.assertEqual(0,score('ＡＢＣ','abc')['character_edits'])
        self.assertEqual(1,score('取消服务','取消业务')['character_edits'])
        self.assertEqual('1$50',normalize('1 $ 50'))
        with self.assertRaises(ValueError):score('!!!','x')


if __name__=='__main__':unittest.main()
