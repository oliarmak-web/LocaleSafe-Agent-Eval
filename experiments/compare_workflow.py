"""Build a concise, reproducible two-model study card from audited results."""
import argparse
import json
from pathlib import Path

from experiments.summarize_workflow import audit, summarize


def study(directories):
    runs = []
    for directory in directories:
        manifest, records, rows = audit(directory)
        runs.append((manifest, summarize(records, rows)))
    left, right = [run[0]["settings"] for run in runs]
    for field in ("cases_sha256", "collector_sha256", "builder_sha256", "shared_scorer_sha256", "repeats", "seed", "temperature", "top_p", "top_k", "max_new_tokens", "enable_thinking", "dtype", "device", "batch_size", "quantization", "torch", "transformers"):
        if left.get(field) != right.get(field):
            raise ValueError(f"unmatched replication setting: {field}")
    return runs


def render(runs):
    names = [m["settings"]["model"]["model"].split("/")[-1] for m, _ in runs]
    summaries = [s for _, s in runs]
    lines = ["# Does language change the agent's action?", "",
             "**1,800 recorded decisions · two related models · five languages · six workflow families.** Free Colab T4; identical float16 runtime, prompts, tasks and decoding settings across models. AI-authored draft translations.", "",
             "[Findings in plain English](FINDINGS.md) · [Why this is credible and useful](WHY_IT_MATTERS.md)", "",
             "## What we ran", "",
             "30 authored scenarios (six templates × five variants), each in English, Spanish, Simplified Chinese, Ukrainian and Haitian Creole. Two stochastic repeats. IDs and slot/day labels stay invariant; locale stays US.", "",
             "| Experiment | Decisions per model | Question |", "|---|---:|---|",
             "| Matched-language baseline | 300 | Does the requested action change with user language? |",
             "| Localized policy | 240 | Does translating the policy help the same request? |",
             "| Canonical structured facts | 60 | Does the failure remain after removing interpretation? |",
             "| Rejected-proposal correction | 300 | Can the model replace a seeded wrong proposal after rejection? |",
             "| English restatement | Reuses baseline | Does an equivalent authored English request succeed? |",
             "| Larger-model replication | Same 900-decision grid | Does the pattern survive a model change? |", "",
             "This is not a human-verified translation-rescue experiment. No translation service was tested. Shared English and structured-fact controls are reused, not counted as extra generations.", "",
             "## Results", "", f"| Condition | {names[0]} strict | {names[1]} strict |", "|---|---:|---:|"]
    for condition in ("baseline", "localized_policy", "structured_facts", "recovery"):
        cells = [s["strict"]["conditions"][condition] for s in summaries]
        lines.append(f"| {condition} | {cells[0]['correct']}/{cells[0]['n']} | {cells[1]['correct']}/{cells[1]['n']} |")
    lines += ["", f"| User language | {names[0]} strict / fence-only | {names[1]} strict / fence-only |", "|---|---:|---:|"]
    for language in ("en", "es", "zh-Hans", "uk", "ht"):
        cells = []
        for s in summaries:
            a = s["strict"]["languages"][language]["baseline"]
            b = s["fence_only"]["languages"][language]["baseline"]
            cells.append(f"{a['correct']}/{a['n']} / {b['correct']}/{b['n']}")
        lines.append(f"| {language} | {cells[0]} | {cells[1]} |")
    lines += ["", "Strict requires one exact-schema JSON call. Fence-only removes just an enclosing Markdown JSON fence; it does not repair arguments or prose. Every recorded call is replayed against the sandbox state.", "",
              "## What English-only checks missed in this run", "",
              "These matched counts use the existing recorded outputs. An English pass paired with a target-language failure identifies a case an English-only check would not expose in this setup. Draft translations prevent attributing that difference solely to language.", "",
              "| Model | Target language | English passed, target failed | Target passed, English failed |", "|---|---|---:|---:|"]
    for name, summary in zip(names, summaries):
        for language, pair in summary["strict"]["contrasts"]["english_vs_target"].items():
            lines.append(f"| {name} | {language} | {pair['left_only']}/{pair['pairs']} | {pair['right_only']}/{pair['pairs']} |")
    lines += ["", "English controls are reused across languages, so these counts must not be summed as independent scenarios. The small model failed all English baseline requests; that floor prevents a useful language-gap estimate. [Evaluation and monitoring implications](MULTILINGUAL_EVAL_MONITORING.md).", "",
              "## Correction by language", "", f"| User language | {names[0]} strict | {names[1]} strict |", "|---|---:|---:|"]
    for language in ("en", "es", "zh-Hans", "uk", "ht"):
        cells = [s["strict"]["languages"][language]["recovery"] for s in summaries]
        lines.append(f"| {language} | {cells[0]['correct']}/{cells[0]['n']} | {cells[1]['correct']}/{cells[1]['n']} |")
    lines += ["", "Correction varies by model and language; the larger model does not uniformly improve it. Draft translations and different conversation histories prevent a general language ranking.", "",
              "## Diagnostic findings", ""]
    for name, s in zip(names, summaries):
        strict = s["strict"]
        a = strict["conditions"]["baseline"]
        b = s["fence_only"]["conditions"]["baseline"]
        pairs = strict["contrasts"]["baseline_vs_structured_facts"]["en"]
        policy = strict["contrasts"]["baseline_vs_localized_policy"]
        helped = sum(p["right_only"] for p in policy.values())
        hurt = sum(p["left_only"] for p in policy.values())
        r = strict["conditions"]["recovery"]
        unauthorized = sum(m["unauthorized_attempts"] for m in strict["conditions"].values())
        lines += [f"**{name}**", "",
                  f"- Format: {a['parsed']}/300 baseline answers meet the schema; fence removal adds {b['correct'] - a['correct']} correct calls.",
                  f"- Structured facts versus English baseline: {pairs['right_only']} control-only successes, {pairs['left_only']} baseline-only successes, {pairs['both_correct']} shared successes and {pairs['both_wrong']} shared failures across 60 matched decisions.",
                  f"- Localized policy: {helped} successes gained and {hurt} lost across 240 matched decisions. Translation and language mixing remain possible explanations.",
                  f"- Correction: {r['correct']}/300 seeded wrong proposals are corrected under strict scoring. This is not recovery from the model's own baseline mistakes.",
                  f"- Parsed unauthorized mutation attempts: {unauthorized}; sandbox safeguards block them. Invalid outputs also fail, so this count alone is not a safety score.", ""]
    lines += ["## How to read the evidence", "",
              "Language-associated differences are leads for independent review. They do not isolate language from translation quality, instruction wording, mixed-language interfaces or model limitations. Strong English/oracle failures weaken a language-only explanation; success after an oracle intervention suggests an interpretation bottleneck but does not uniquely identify its cause.", "",
              "All tasks withhold approval. The correction condition uses an injected reachable proposal and a scripted user response, and supplies a valid JSON example. Baseline-versus-correction differences cannot separate correction skill from example-driven format adherence or other history effects. This tests bounded tool decisions and controlled correction, not autonomous end-to-end agents, positive consent, cultural competence or real-world harm.", "",
              "The effective diversity is six template families, not 1,800 independent situations. No confidence intervals, significance, language rankings, equivalence or population-level fairness claims. Two models from one family are a limited replication.", "",
              "## Original contribution and next test", "",
              "LocaleSafe contributes authored service scenarios, executable state checks and matched interventions that separate interface, interpretation and workflow outcomes. It does not claim to invent multilingual evaluation or failure decomposition.", "",
              "Next: independently review translations, add held-out scenarios and positive approval cases, collect genuinely interactive episodes, and replicate with another model family. Cultural context needs separately reviewed cases; script coverage alone does not establish it.", "",
              "[Raw outputs, source and hashes](../experiments/README.md#latest-matched-workflow-study) · [Frozen protocol and amendments](../experiments/workflow/PROTOCOL.md) · [Execution history](../experiments/workflow/EXECUTION_HISTORY.md) · [Benchmark registry](BENCHMARKS.md)"]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directories", nargs=2, type=Path)
    parser.add_argument("--output", type=Path, default=Path("docs/WORKFLOW_STUDY.md"))
    args = parser.parse_args()
    runs = study(args.directories)
    args.output.write_text(render(runs), encoding="utf-8")
    print(f"Wrote audited study card: {args.output}")


if __name__ == "__main__":
    main()
