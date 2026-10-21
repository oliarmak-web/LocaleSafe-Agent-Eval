"""Audit and summarize the controlled, closed-choice attribution probe."""

import argparse
import hashlib
import itertools
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

from localesafe.attribution_probe import assess, paired_seed, prompt_for, validate_tasks
from localesafe.evaluate import read_jsonl, sha256
from localesafe.service_eval import date_context


def correct_index(task):
    if task["kind"] == "interpretation":
        return task["options"].index(date_context(task["case"])[0])
    return next(i for i in range(3) if assess(task, i)["passed"])


def audit(directory):
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if manifest["status"] != "completed":
        raise ValueError("incomplete experiment")
    for name in ("tasks", "attempts"):
        if sha256(directory / f"{name}.jsonl") != manifest[name + "_sha256"]:
            raise ValueError("artifact hash mismatch")
    raw_lines = (directory / "attempts.jsonl").read_bytes().splitlines(keepends=True)
    for resume in manifest.get("resumes", []):
        prefix = b"".join(raw_lines[:resume["preserved_choices"]])
        if hashlib.sha256(prefix).hexdigest() != resume["prior_log_sha256"]:
            raise ValueError("preserved pre-resume records changed")
    tasks = read_jsonl(directory / "tasks.jsonl")
    validate_tasks(tasks)
    indexed = {t["case"]["id"]: t for t in tasks}
    attempts = read_jsonl(directory / "attempts.jsonl")
    expected = {(key, p, draw) for key in indexed for p in itertools.permutations(range(3)) for draw in range(manifest["draws_per_order"])}
    seen = set()
    for row in attempts:
        key = row["id"], tuple(row["order"]), row["draw"]
        if key not in expected or key in seen:
            raise ValueError("unknown/duplicate attempt")
        seen.add(key)
        task = indexed[row["id"]]
        metadata = {"kind": task["kind"], "family": task["case"]["family"], "language": task["case"]["language"],
                    "locale": task["case"]["locale"], "phrase": task["phrase"]}
        if any(row[key] != value for key, value in metadata.items()):
            raise ValueError("attempt metadata mismatch")
        if row["messages"] != prompt_for(task, tuple(row["order"])):
            raise ValueError("prompt mismatch")
        seed = paired_seed(task, tuple(row["order"]), row["draw"], manifest["seed"])
        label = random.Random(seed).choices(range(3), weights=row["probabilities_ABC"], k=1)[0]
        if row["seed"] != seed or row["chosen_label"] != "ABC"[label] or row["selected_option"] != row["order"][label]:
            raise ValueError("choice cannot be reproduced")
        if row["score"] != assess(task, row["selected_option"]):
            raise ValueError("score mismatch")
        right = correct_index(task)
        row["correct_choice"] = row["selected_option"] == right
        row["probability_correct"] = row["probabilities_ABC"][row["order"].index(right)]
    if seen != expected:
        raise ValueError("missing attempts")
    return manifest, tasks, attempts


def metrics(rows):
    return {"sampled_correct": sum(r["correct_choice"] for r in rows), "choices": len(rows),
            "mean_probability_correct": sum(r["probability_correct"] for r in rows) / len(rows),
            "distinct_items": len({r["id"] for r in rows})}


def contrasts(rows, axis):
    grouped = defaultdict(dict)
    for row in rows:
        key = (row["family"], row["locale"], tuple(row["order"]), row["draw"])
        if axis == "language":
            key += (row["phrase"],)
            side = row["language"]
        else:
            key += (row["language"],)
            side = row["phrase"]
        grouped[key][side] = row
    left, right = ("en", "es") if axis == "language" else (0, 1)
    counts = {"pairs": 0, "both_correct": 0, "both_wrong": 0, "left_correct_right_wrong": 0,
              "left_wrong_right_correct": 0, "mean_probability_left_minus_right": 0.0}
    for pair in grouped.values():
        if set(pair) != {left, right}:
            raise ValueError("incomplete contrast")
        a, b = pair[left], pair[right]
        counts["pairs"] += 1
        key = ("both_correct" if a["correct_choice"] and b["correct_choice"] else
               "both_wrong" if not a["correct_choice"] and not b["correct_choice"] else
               "left_correct_right_wrong" if a["correct_choice"] else "left_wrong_right_correct")
        counts[key] += 1
        counts["mean_probability_left_minus_right"] += a["probability_correct"] - b["probability_correct"]
    counts["mean_probability_left_minus_right"] /= counts["pairs"]
    return counts


def summarize(directory):
    directory = Path(directory)
    manifest, tasks, attempts = audit(directory)
    interpretation = [r for r in attempts if r["kind"] == "interpretation"]
    workflow = [r for r in attempts if r["kind"] == "workflow"]
    summary = {"interpretation_by_language": {lang: metrics([r for r in interpretation if r["language"] == lang]) for lang in ("en", "es")},
               "interpretation_by_locale": {locale: metrics([r for r in interpretation if (r["locale"] or "unspecified") == locale]) for locale in ("US", "GB", "unspecified")},
               "workflow": metrics(workflow),
               "workflow_by_task": {task["case"]["family"]: metrics([r for r in workflow if r["family"] == task["case"]["family"]]) for task in tasks if task["kind"] == "workflow"},
               "language_pairs_en_vs_es": contrasts(interpretation, "language"),
               "phrasing_pairs_p0_vs_p1": {lang: contrasts([r for r in interpretation if r["language"] == lang], "phrasing") for lang in ("en", "es")}}
    # Diagnose label-position sensitivity without pretending options are calibrated confidence.
    forwards = {}
    indexed = {t["case"]["id"]: t for t in tasks}
    position = defaultdict(list)
    for row in attempts:
        key = row["id"], tuple(row["order"])
        if key in forwards:
            continue
        forwards[key] = row
        letter = "ABC"[row["order"].index(correct_index(indexed[row["id"]]))]
        position[(row["kind"], letter)].append(row)
    summary["correct_option_position"] = {f"{kind}-{label}": metrics(rows) for (kind, label), rows in sorted(position.items())}
    summary["oracle_controls"] = {"passed": sum(assess(t, correct_index(t))["passed"] for t in tasks), "tasks": len(tasks)}
    summary["chosen_label_counts"] = {kind: dict(Counter(r["chosen_label"] for r in attempts if r["kind"] == kind))
                                      for kind in ("interpretation", "workflow")}
    (directory / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    lines = ["# Language or workflow? Controlled results", "",
             f"Model: `{manifest['model']}`. {len(tasks)} tasks; {len(forwards)} forward passes; {len(attempts)} sampled choices. No paid API.", "",
             "**Scope:** closed-choice recognition, not a live agent. Formatting is fixed by design. Translations are draft. Repeated choices are not independent tasks.", "",
             f"**Lead finding:** strong answer-position sensitivity limits attribution. The workflow probe chose A in {summary['chosen_label_counts']['workflow'].get('A', 0)}/{len(workflow)} draws despite balanced correct-answer positions. Check the response method before attributing failures to language or workflow comprehension.", "",
             "## Interpretation", "", "| Language | Items | Correct / sampled choices | Mean probability on correct option |", "|---|---:|---:|---:|"]
    for lang, m in summary["interpretation_by_language"].items():
        lines.append(f"| {lang} | {m['distinct_items']} | {m['sampled_correct']}/{m['choices']} | {m['mean_probability_correct']:.1%} |")
    lines += ["", "Probabilities are conditional on the three offered tokens, not calibrated confidence or free-form accuracy. Uniform-choice reference: 33.3%; no inferential test is claimed.", "",
              "| Explicit locale | Correct / choices | Mean correct-option probability |", "|---|---:|---:|"]
    for locale, m in summary["interpretation_by_locale"].items():
        lines.append(f"| {locale} | {m['sampled_correct']}/{m['choices']} | {m['mean_probability_correct']:.1%} |")
    pair = summary["language_pairs_en_vs_es"]
    lines += ["", f"Matched draws: English-only correct **{pair['left_correct_right_wrong']}**; Spanish-only correct **{pair['left_wrong_right_correct']}**; both wrong **{pair['both_wrong']}**; both correct **{pair['both_correct']}**.", "",
              "| Phrasing control | P0-only correct | P1-only correct | Mean P0−P1 probability |", "|---|---:|---:|---:|"]
    for lang, m in summary["phrasing_pairs_p0_vs_p1"].items():
        lines.append(f"| {lang} | {m['left_correct_right_wrong']} | {m['left_wrong_right_correct']} | {m['mean_probability_left_minus_right']:.1%} |")
    lines += ["", "## Workflow with known facts", "", "English-only controls remove translation/date extraction. The model selects a plan; the sandbox executes it.", "",
              "| Rule | Correct / choices | Mean correct-option probability |", "|---|---:|---:|"]
    for name, m in summary["workflow_by_task"].items():
        lines.append(f"| {name.removeprefix('workflow-')} | {m['sampled_correct']}/{m['choices']} | {m['mean_probability_correct']:.1%} |")
    m = summary["workflow"]
    lines += ["", f"Workflow total: **{m['sampled_correct']}/{m['choices']}** choices correct. Canonical correct actions pass **{summary['oracle_controls']['passed']}/{summary['oracle_controls']['tasks']}** simulator controls.", "",
              "## Answer-position control", "", "Mean probability on the correct option, grouped by its label. Large differences indicate position sensitivity even though aggregate orders are balanced.", "",
              "| Probe | Correct at A | Correct at B | Correct at C |", "|---|---:|---:|---:|"]
    for kind in ("interpretation", "workflow"):
        values = [summary["correct_option_position"][f"{kind}-{label}"]["mean_probability_correct"] for label in "ABC"]
        lines.append(f"| {kind} | {values[0]:.1%} | {values[1]:.1%} | {values[2]:.1%} |")
    workflow_finding = (f"English-only plan selection failed in {m['choices'] - m['sampled_correct']}/{m['choices']} sampled choices; translation is not required for those failures."
                        if m["sampled_correct"] < m["choices"] else "No English workflow-control failure was observed; this does not establish general workflow reliability.")
    lines += ["",
              "## What this establishes", "",
              "- Format errors cannot explain failures in this constrained probe.",
              "- " + workflow_finding + " Label bias prevents attributing these errors specifically to workflow understanding.",
              "- Language and phrasing contrasts identify candidates for review, not causal population effects.",
              "- Perfect canonical replay validates these controls, not production workflow reliability.", "",
              "## Limits", "", "Two date families; six workflow tasks; one small model; draft translations; offered answers; no interactive planning. Difficulty differs between probes, so their error rates cannot allocate a single causal share to language versus workflow. No significance/equivalence claims. Next: human review, held-out families, more models, free-form and interactive replications.", "",
              "Evidence: `tasks.jsonl`, exact prompts/probabilities/seeds/scores in `attempts.jsonl`, settings/hashes in `manifest.json`, position diagnostics in `summary.json`. The protocol was frozen before collection; this descriptive analysis was written during the run.", ""]
    (directory / "INSIGHTS.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    summarize(parser.parse_args().directory)
