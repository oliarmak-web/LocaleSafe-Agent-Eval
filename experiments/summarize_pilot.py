"""Generate a descriptive report from completed, inspectable model artifacts."""

import argparse
import json
import statistics
from pathlib import Path

from localesafe.evaluate import read_jsonl, sha256
from localesafe.collect_local import parse_prediction, summarize_attempts


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
             "These are genuine local model outputs on public draft scenarios. This is an exploratory comparison of two prompts on one model, not two independent studies. No API inference fee was incurred. No tools were executed.", "",
             "## Results", "", "| Language | Cases per condition | Baseline pass | Check pass |",
             "|---|---:|---:|---:|"]
    for language in reports["baseline"]["languages"]:
        before = reports["baseline"]["languages"][language]
        after = reports["check"]["languages"][language]
        lines.append(f"| {language} | {before['n']} | {before['pass_rate']:.1%} | {after['pass_rate']:.1%} |")
    lines += ["", "Passing requires the expected decision AND exact proposed tool calls/arguments. Invalid JSON or invalid schemas count as failures in these denominators.", "",
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
              + ", ".join(f"{name}={count}" for name, count in fence_counts.items()) + ". This diagnostic was added after observing an early fenced answer; it was not a preregistered outcome. Strict failures conflate format compliance and decision behavior, so do not interpret them all as safety failures."]
    lines += ["", "Secondary, post-hoc fence-only parsing analysis (same raw generations, no new model calls):", "",
              "| Condition | Pass / all after fence-only removal | Still invalid |", "|---|---:|---:|"]
    for name, report in diagnostics.items():
        lines.append(f"| {name} | {sum(r['passed'] for r in report['cases'])}/{report['n']} | {report['invalid_generations']} |")
    lines += ["", "This secondary analysis removes only an exact surrounding Markdown JSON fence. It changes neither decisions nor tool arguments. It must not replace the primary strict result or be represented as a new independent experiment. Per-case secondary scores are in `posthoc-format-report.json`."]
    (directory / "posthoc-format-report.json").write_text(json.dumps(diagnostics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    baseline = {r["id"]: r for r in reports["baseline"]["cases"]}
    check = {r["id"]: r for r in reports["check"]["cases"]}
    improved = [key for key in baseline if not baseline[key]["passed"] and check[key]["passed"]]
    worsened = [key for key in baseline if baseline[key]["passed"] and not check[key]["passed"]]
    lines += ["", f"Check prompt changed {len(improved)} case(s) from fail to pass and {len(worsened)} from pass to fail.", "",
              "Improved IDs: " + (", ".join(f"`{x}`" for x in improved) or "none") + ".", "",
              "Regressed IDs: " + (", ".join(f"`{x}`" for x in worsened) or "none") + ".", "",
              "## Interpretation limits", "",
              "Only six scenario families underpin the language rows; those translations are correlated observations, not 54 independent scenarios. Non-English translations and all policy labels still need independent review. Public examples, one small model, one sampled attempt, and no uncertainty analysis cannot establish general safety, bias, statistical significance, or intervention effectiveness. The check condition may regress. Both positive and negative outcomes are retained.", "",
              "This evaluates JSON decision generation, not native function calling, actual dispatch, clinical correctness, ASR, or speech. A stronger next study needs reviewed, newly authored held-out families, repeated runs, larger comparison models, and family-level paired uncertainty analysis.", "",
              "## Artifacts", "",
              "- `manifest.json`: exact policy, intervention, model revision, versions, seeds, decoding, and source hashes.",
              "- `cases.jsonl`: the frozen input cases and expected labels (labels never entered prompts).",
              "- `attempts.jsonl`: every exact prompt, raw model answer, generation status, token count, latency, and seed.",
              "- `baseline-report.json` / `check-report.json`: per-case scoring including invalid attempts.", "",
              f"Attempt log SHA-256: `{manifest['attempts_sha256']}`.", ""]
    (directory / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    summarize(parser.parse_args().directory)
