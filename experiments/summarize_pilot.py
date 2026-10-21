"""Generate a descriptive report from completed, inspectable model artifacts."""

import argparse
import json
import statistics
from pathlib import Path

from localesafe.evaluate import read_jsonl, sha256
from localesafe.collect_local import parse_prediction, summarize_attempts
from localesafe.diagnose import write_diagnosis


def summarize(directory):
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "completed":
        raise ValueError("cannot summarize an incomplete experiment")
    if manifest["attempts_sha256"] != sha256(directory / "attempts.jsonl"):
        raise ValueError("attempt artifact hash mismatch")
    reports = {name: json.loads((directory / f"{name}-report.json").read_text(encoding="utf-8"))
               for name in ("baseline", "check")}
    attempts = read_jsonl(directory / "attempts.jsonl")
    cases = read_jsonl(directory / "cases.jsonl")
    case_index = {c["id"]: c for c in cases}
    if manifest["cases_sha256"] != sha256(directory / "cases.jsonl"):
        raise ValueError("case artifact hash mismatch")
    for condition, report in reports.items():
        recomputed = summarize_attempts(cases, [a for a in attempts if a["condition"] == condition])
        if recomputed != report:
            raise ValueError("report does not match raw attempt artifacts")
    lines = ["# Local model pilot — descriptive results", "",
             f"Model: `{manifest['model']}`; revision `{manifest['revision']}`.", "",
             f"Completed: {manifest['completed_utc']}. CPU float32; one sampled generation per case/condition.", "",
             "Two prompts, one local model. No paid inference or tool execution.", "",
             "Strict failures include formatting. Read [stage diagnostics](LANGUAGE_DIAGNOSTICS.md) before interpreting language differences. Custom suite only; no causal or external-benchmark claim.", "",
             "## Results", "", "| Language | Cases per condition | Baseline pass | Check pass |",
             "|---|---:|---:|---:|"]
    for language in reports["baseline"]["languages"]:
        before = reports["baseline"]["languages"][language]
        after = reports["check"]["languages"][language]
        lines.append(f"| {language} | {before['n']} | {before['pass_rate']:.1%} | {after['pass_rate']:.1%} |")
    lines += ["", "Pass = correct decision and exact calls/arguments. Invalid outputs count as failures.", "",
              "| Condition | Passed / all | Invalid generations | Missed / valid urgent outputs | Unnecessary / valid nonurgent outputs | Median generation seconds |",
              "|---|---:|---:|---:|---:|---:|"]
    for name, report in reports.items():
        rows = [a for a in attempts if a["condition"] == name]
        missed = sum(r["missed_escalation"] is True for r in report["cases"])
        extra = sum(r["unnecessary_escalation"] is True for r in report["cases"])
        passed = sum(r["passed"] for r in report["cases"])
        urgent_n = sum(r["generation_valid"] and case_index[r["id"]]["expected"]["decision"] == "escalate" for r in report["cases"])
        nonurgent_n = sum(r["generation_valid"] and case_index[r["id"]]["expected"]["decision"] != "escalate" for r in report["cases"])
        lines.append(f"| {name} | {passed}/{report['n']} | {report['invalid_generations']} | {missed}/{urgent_n} | {extra}/{nonurgent_n} | {statistics.median(r['latency_seconds'] for r in rows):.2f} |")
    # Post-hoc descriptive diagnosis: never alters the primary strict scores.
    fence_counts = {}
    diagnostics = {}
    for name in reports:
        count = 0
        diagnostic_attempts = []
        for attempt in attempts:
            if attempt["condition"] != name:
                continue
            diagnostic_attempts.append(dict(attempt))
            raw = attempt.get("raw_output", "")
            if attempt.get("status") != "invalid":
                continue
            if raw.startswith("```json\n") and raw.endswith("\n```"):
                try:
                    diagnostic_attempts[-1]["prediction"] = parse_prediction(raw[8:-4].strip(), case_index[attempt["id"]])
                    count += 1
                except (ValueError, TypeError):
                    pass
        fence_counts[name] = count
        diagnostics[name] = summarize_attempts(cases, diagnostic_attempts)
    lines += ["", "Post-hoc formatting diagnostic (no score repair): invalid answers containing schema-valid JSON wrapped only in a Markdown JSON fence: "
              + ", ".join(f"{name}={count}" for name, count in fence_counts.items()) + ". Added after initial output inspection; not preregistered. Formatting failure is not itself a safety failure."]
    lines += ["", "Secondary, post-hoc fence-only parsing analysis (same raw generations, no new model calls):", "",
              "| Condition | Pass / all after fence-only removal | Still invalid |", "|---|---:|---:|"]
    for name, report in diagnostics.items():
        lines.append(f"| {name} | {sum(r['passed'] for r in report['cases'])}/{report['n']} | {report['invalid_generations']} |")
    lines += ["", "Fence-only parsing changes no decisions or arguments. This post-hoc diagnostic is not a new experiment or replacement score. Details: `posthoc-format-report.json`."]
    (directory / "posthoc-format-report.json").write_text(json.dumps(diagnostics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    baseline = {r["id"]: r for r in reports["baseline"]["cases"]}
    check = {r["id"]: r for r in reports["check"]["cases"]}
    improved = [key for key in baseline if not baseline[key]["passed"] and check[key]["passed"]]
    worsened = [key for key in baseline if baseline[key]["passed"] and not check[key]["passed"]]
    lines += ["", f"Check prompt changed {len(improved)} case(s) from fail to pass and {len(worsened)} from pass to fail.", "",
              "Improved IDs: " + (", ".join(f"`{x}`" for x in improved) or "none") + ".", "",
              "Regressed IDs: " + (", ".join(f"`{x}`" for x in worsened) or "none") + ".", "",
              "## Interpretation limits", "",
              "Six families; draft translations; one model; one generation per item/condition. Translations are clustered observations. No validated safety, bias, significance, or intervention-efficacy claim.", "",
              "Measures JSON decision generation. Next: reviewed held-out families, repeated runs, comparison models, and family-level uncertainty.", "",
              "## Artifacts", "",
              "- `manifest.json`: exact policy, intervention, model revision, versions, seeds, decoding, and source hashes.",
              "- `cases.jsonl`: the frozen input cases and expected labels (labels never entered prompts).",
              "- `attempts.jsonl`: every exact prompt, raw model answer, generation status, token count, latency, and seed.",
              "- `baseline-report.json` / `check-report.json`: per-case scoring including invalid attempts.", "",
              f"Attempt log SHA-256: `{manifest['attempts_sha256']}`.", ""]
    (directory / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8")
    write_diagnosis(cases, attempts, directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    summarize(parser.parse_args().directory)
