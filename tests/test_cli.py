import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_report_provenance_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            command = [sys.executable, "-m", "localesafe.cli", "--cases", "examples/cases.jsonl",
                       "--responses", "examples/synthetic-failures.jsonl", "--output", str(output),
                       "--run-label", "synthetic-fixture-not-a-model"]
            first = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = output.read_bytes()
            report = json.loads(original)
            self.assertEqual(report["n"], 18)
            self.assertEqual(len(report["provenance"]["cases_sha256"]), 64)
            self.assertTrue(report["translation_warning"])
            second = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(second.returncode, 2)
            self.assertEqual(output.read_bytes(), original)

    def test_invalid_artifact_produces_no_report(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "invalid.jsonl"
            source.write_text('{"id":"missing-fields"}\n', encoding="utf-8")
            output = Path(directory) / "report.json"
            result = subprocess.run([sys.executable, "-m", "localesafe.cli", "--cases", str(source),
                                     "--responses", "examples/synthetic-perfect.jsonl", "--output", str(output),
                                     "--run-label", "invalid"], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(output.exists())
