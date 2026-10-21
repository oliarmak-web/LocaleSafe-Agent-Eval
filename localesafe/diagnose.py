"""Descriptive stage attribution and paired language outcomes, not causal inference."""

import json

from .collect_local import parse_prediction, summarize_attempts


def diagnose(cases, attempts):
    output = {"interpretation": "Language-associated disagreements are descriptive, not proof of a language effect.",
              "conditions": {}}
    for condition in sorted({a["condition"] for a in attempts}):
        rows = [a for a in attempts if a["condition"] == condition]
        summarize_attempts(cases, rows)  # Require complete coverage before attribution.
        indexed = {a["id"]: a for a in rows}
        parsers = {}
        for parser in ("strict", "fence_only_posthoc"):
            scored = []
            for case in cases:
                attempt = indexed[case["id"]]
                prediction = attempt.get("prediction")
                recovered = False
                raw = attempt.get("raw_output", "")
                if prediction is None and parser == "fence_only_posthoc" and raw.startswith("```json\n") and raw.endswith("\n```"):
                    try:
                        prediction = parse_prediction(raw[8:-4].strip(), case)
                        recovered = True
                    except (ValueError, TypeError):
                        pass
                decision = prediction["decision"] == case["expected"]["decision"] if prediction else None
                calls = (sorted(json.dumps(c, sort_keys=True, ensure_ascii=False) for c in prediction["tool_calls"])
                         == sorted(json.dumps(c, sort_keys=True, ensure_ascii=False) for c in case["expected"]["tool_calls"])) if prediction else None
                scored.append({"id": case["id"], "pair_id": case["pair_id"], "language": case["language"],
                               "format_valid": prediction is not None, "fence_recovered": recovered,
                               "decision_correct": decision, "tools_correct": calls,
                               "passed": decision is True and calls is True})
            language_metrics = {}
            for language in sorted({c["language"] for c in cases}):
                subset = [r for r in scored if r["language"] == language]
                language_metrics[language] = {"n": len(subset),
                    "format_failures": sum(not r["format_valid"] for r in subset),
                    "decision_errors_among_parseable": sum(r["decision_correct"] is False for r in subset),
                    "tool_errors_among_parseable": sum(r["tools_correct"] is False for r in subset),
                    "parseable_n": sum(r["format_valid"] for r in subset)}
            pairs = {}
            for language in language_metrics:
                if language == "en":
                    continue
                counts = {"both_pass": 0, "both_fail": 0, "english_pass_other_fail": 0,
                          "english_fail_other_pass": 0, "unparseable_pair": 0,
                          "both_parseable_n": 0, "english_decision_correct_other_wrong": 0,
                          "english_decision_wrong_other_correct": 0}
                for row in [r for r in scored if r["language"] == language]:
                    en = next(r for r in scored if r["pair_id"] == row["pair_id"] and r["language"] == "en")
                    key = ("both_pass" if en["passed"] and row["passed"] else "both_fail" if not en["passed"] and not row["passed"]
                           else "english_pass_other_fail" if en["passed"] else "english_fail_other_pass")
                    counts[key] += 1
                    if en["format_valid"] and row["format_valid"]:
                        counts["both_parseable_n"] += 1
                        counts["english_decision_correct_other_wrong"] += en["decision_correct"] and not row["decision_correct"]
                        counts["english_decision_wrong_other_correct"] += not en["decision_correct"] and row["decision_correct"]
                    else:
                        counts["unparseable_pair"] += 1
                pairs[language] = counts
            parsers[parser] = {"languages": language_metrics, "paired_with_english": pairs, "cases": scored}
        output["conditions"][condition] = parsers
    return output


def write_diagnosis(cases, attempts, directory):
    result = diagnose(cases, attempts)
    (directory / "language-diagnostics.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Language versus workflow: exploratory diagnostics", "",
             "These comparisons do not establish a causal language effect. Six scenario families, draft translations, one model, and one generation per item cannot disentangle language, translation, phrasing, sampling, and prompt sensitivity.", "",
             "The strict analysis measures the complete output contract. Fence-only parsing is a post-hoc diagnostic on the exact same generations. No model decisions or arguments are changed. Decision/tool errors below are conditional on parseable outputs; missing/unparseable decisions are unknown, not inferred errors. Error categories overlap.", ""]
    for condition, parsers in result["conditions"].items():
        for parser, metrics in parsers.items():
            lines += [f"## {condition} / {parser}", "",
                      "| Language | All | Parseable | Format failures | Decision errors / parseable | Tool errors / parseable |",
                      "|---|---:|---:|---:|---:|---:|"]
            for language, row in metrics["languages"].items():
                lines.append(f"| {language} | {row['n']} | {row['parseable_n']} | {row['format_failures']} | {row['decision_errors_among_parseable']}/{row['parseable_n']} | {row['tool_errors_among_parseable']}/{row['parseable_n']} |")
            lines += ["", "Paired complete-task outcomes versus the same English scenario:", "",
                      "| Language | Both pass | Both fail | English pass / other fail | English fail / other pass | Pairs with unparseable output |",
                      "|---|---:|---:|---:|---:|---:|"]
            for language, row in metrics["paired_with_english"].items():
                lines.append(f"| {language} | {row['both_pass']} | {row['both_fail']} | {row['english_pass_other_fail']} | {row['english_fail_other_pass']} | {row['unparseable_pair']} |")
            lines += ["", "Unparseable-pair counts overlap the pass/fail columns. English-pass/other-fail is a candidate language-associated counterexample; inspect the raw case and translation before attribution. Both-fail is a shared failure, not proof of a particular workflow bug. JSON includes decision-only paired discordances and their parseable-pair denominator.", ""]
    lines += ["## Benchmarks and next controls", "", "See `docs/BENCHMARKS.md` for the exact custom-suite status, external benchmarks not yet run, and the next controlled study design. Add reviewed parallel inputs, English paraphrase controls, repeated generations, a canonical tool-simulator control, and constrained-output comparisons before attributing an effect to language.", ""]
    (directory / "LANGUAGE_DIAGNOSTICS.md").write_text("\n".join(lines), encoding="utf-8")
