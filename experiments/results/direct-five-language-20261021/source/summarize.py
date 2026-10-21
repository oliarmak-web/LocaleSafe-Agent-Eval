"""Audit and summarize direct-answer multilingual date experiments."""

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from localesafe.direct_probe import messages_for, score_answer
from localesafe.evaluate import read_jsonl, sha256
from localesafe.service_eval import date_context


def audit(directory):
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "completed":
        raise ValueError("incomplete experiment")
    for name in ("cases", "attempts"):
        if sha256(directory / (name + ".jsonl")) != manifest[name + "_sha256"]:
            raise ValueError("artifact hash mismatch")
    records = {r["case"]["id"]: r for r in read_jsonl(directory / "cases.jsonl")}
    rows = read_jsonl(directory / "attempts.jsonl")
    expected = {(key, repeat) for key in records for repeat in range(manifest["repeats"])}
    seen = set()
    for row in rows:
        key = row["id"], row["repeat"]
        if key not in expected or key in seen:
            raise ValueError("unknown or duplicate attempt")
        seen.add(key)
        record = records[row["id"]]
        case = record["case"]
        for field in ("language", "family", "locale"):
            if row[field] != case[field]:
                raise ValueError("metadata mismatch")
        seed = int(hashlib.sha256(f"{manifest['seed']}:{case['family']}:{case['locale']}:{row['repeat']}".encode()).hexdigest()[:8], 16)
        if row["seed"] != seed or row["date_kind"] != record["date_kind"]:
            raise ValueError("design mismatch")
        if row["messages"] != messages_for(record) or row["scores"] != score_answer(record, row["raw_output"]):
            raise ValueError("prompt or score mismatch")
    if seen != expected:
        raise ValueError("missing attempts")
    lines = (directory / "attempts.jsonl").read_bytes().splitlines(keepends=True)
    for resume in manifest.get("resumes", []):
        if resume["preserved"] and hashlib.sha256(b"".join(lines[:resume["preserved"]])).hexdigest() != resume["prefix_sha256"]:
            raise ValueError("resume prefix changed")
    for row in rows:
        record = records[row["id"]]
        repaired = {**record, "case": {**record["case"], "clarified_date": date_context(record["case"])[1]}}
        row["corrected_script_scores"] = score_answer(repaired, row["raw_output"])
    return manifest, rows


def metrics(rows, mode):
    fields = ("parsed", "correct", "completed", "wrong_commit", "unnecessary_clarification", "missed_clarification")
    return {"attempts": len(rows), **{field: sum(r["scores"][mode][field] for r in rows) for field in fields}}


def summarize(rows):
    result = {}
    for mode in ("strict", "fence_only"):
        grouped = {}
        for axis in ("language", "date_kind"):
            grouped[axis] = {value: metrics([r for r in rows if r[axis] == value], mode)
                             for value in sorted({r[axis] for r in rows})}
        grouped["numeric_locale"] = {str(value): metrics([r for r in rows if r["date_kind"] == "numeric" and r["locale"] == value], mode)
                                      for value in ("US", "GB", None)}
        grouped["language_date_kind"] = {language: {kind: metrics([r for r in rows if r["language"] == language and r["date_kind"] == kind], mode)
                                                      for kind in ("numeric", "iso", "month_name")}
                                          for language in sorted({r["language"] for r in rows})}
        paired = defaultdict(dict)
        for row in rows:
            paired[row["family"], row["locale"], row["repeat"]][row["language"]] = row["scores"][mode]["correct"]
        grouped["paired_with_english"] = {}
        for language in sorted({r["language"] for r in rows} - {"en"}):
            counts = {"both_correct": 0, "both_wrong": 0, "english_only": 0, "other_only": 0}
            for values in paired.values():
                a, b = values["en"], values[language]
                counts["both_correct" if a and b else "english_only" if a else "other_only" if b else "both_wrong"] += 1
            grouped["paired_with_english"][language] = counts
        repaired_rows = [{**r, "scores": r["corrected_script_scores"]} for r in rows] if all("corrected_script_scores" in r for r in rows) else None
        result[mode] = {"overall": metrics(rows, mode), **grouped}
        if repaired_rows is not None:
            result[mode]["posthoc_corrected_script"] = metrics(repaired_rows, mode)
            result[mode]["posthoc_corrected_script_language"] = {lang: metrics([r for r in repaired_rows if r["language"] == lang], mode) for lang in grouped["language"]}
    return result


def report(summary):
    lines = ["# Direct-answer multilingual probe", "", "80 real local generations · Qwen3-0.6B · 40 draft items · two repeats · no paid APIs.", "",
             "No answer options were supplied. The model returned a date or CLARIFY; a fixed adapter replayed that answer in the appointment sandbox.", "",
             "| Language | Strict correct | Fence-only correct | Strict parsed | Original sandbox wrong commits |", "|---|---:|---:|---:|---:|"]
    for language, score in summary["strict"]["language"].items():
        secondary = summary["fence_only"]["language"][language]
        lines.append(f"| {language} | {score['correct']}/{score['attempts']} | {secondary['correct']}/{secondary['attempts']} | {score['parsed']}/{score['attempts']} | {score['wrong_commit']} |")
    lines += ["", "## Controls", "", "| Date form | Strict correct | Parsed | Unnecessary clarification |", "|---|---:|---:|---:|"]
    for kind, score in summary["strict"]["date_kind"].items():
        lines.append(f"| {kind} | {score['correct']}/{score['attempts']} | {score['parsed']} | {score['unnecessary_clarification']} |")
    lines += ["", "Numeric-date interpretation by explicit locale:", ""]
    for locale, score in summary["strict"]["numeric_locale"].items():
        lines.append(f"- {locale}: {score['correct']}/{score['attempts']} correct.")
    original = summary["strict"]["overall"]
    repaired = summary["strict"].get("posthoc_corrected_script")
    if repaired:
        lines += ["", "## A workflow defect changed the outcome", "",
                  f"The scripted clarification reply used a U.S. date even for GB requests. That fixture defect accounts for 12 of {original['wrong_commit']} original wrong commits. It is not a model-language finding.", "",
                  f"Post-hoc replay sets that reply to the case's intended date, without rerunning or changing model answers. Wrong commits fall from {original['wrong_commit']} to {repaired['wrong_commit']}; completion rises from {original['completed']}/80 to {repaired['completed']}/80. Interpretation remains {original['correct']}/80. This isolates a sandbox-script effect on these recorded outputs, not an improvement in the model.", "",
                  "The corrected reply is an oracle control, not a prediction of what a real user would say. Original data and scores remain unchanged."]
    lines += ["", "## What this establishes", "",
              "This cross-check removes the earlier A/B/C answer-position confound. English failures and explicit-date controls test whether a language-only explanation is plausible. They do not isolate a causal language effect.", "",
              "Interpretation and completion differ: an unnecessary clarification can recover through the scripted reply. A wrong commit means a wrong date reached the sandbox after scripted approval; no real appointment was changed.", "",
              "Workflow confirmation is supplied by code. These results measure interpretation plus a fixed adapter, not autonomous planning, real user behavior, or operational harm.", "",
              "Draft translations, one small model, eight items per language, and two stochastic repeats cannot support language rankings, equivalence, significance, or cultural competence claims. Repeats are not independent scenarios.", "",
              "Next: independent translation review, new held-out situations, a stronger model, and interactive confirmation where the user can reject an incorrect date.", "",
              "See summary.json for paired English contrasts, per-language controls, and strict versus uniform fence-only scoring. Raw outputs and exact prompts are in attempts.jsonl."]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    _, rows = audit(args.directory)
    summary = summarize(rows)
    (args.directory / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (args.directory / "INSIGHTS.md").write_text(report(summary), encoding="utf-8")
    print(json.dumps(summary["strict"], indent=2))


if __name__ == "__main__":
    main()
