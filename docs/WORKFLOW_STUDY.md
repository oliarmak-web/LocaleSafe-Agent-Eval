# Does language change the agent's action?

**1,800 recorded decisions · two related models · five languages · six workflow families.** Free Colab T4; identical float16 runtime, prompts, tasks and decoding settings across models. AI-authored draft translations.

[Findings in plain English](FINDINGS.md) · [Why this is credible and useful](WHY_IT_MATTERS.md)

## What we ran

30 authored scenarios (six templates × five variants), each in English, Spanish, Simplified Chinese, Ukrainian and Haitian Creole. Two stochastic repeats. IDs and slot/day labels stay invariant; locale stays US.

| Experiment | Decisions per model | Question |
|---|---:|---|
| Matched-language baseline | 300 | Does the requested action change with user language? |
| Localized policy | 240 | Does translating the policy help the same request? |
| Canonical structured facts | 60 | Does the failure remain after removing interpretation? |
| Rejected-proposal correction | 300 | Can the model replace a seeded wrong proposal after rejection? |
| English restatement | Reuses baseline | Does an equivalent authored English request succeed? |
| Larger-model replication | Same 900-decision grid | Does the pattern survive a model change? |

This is not a human-verified translation-rescue experiment. No translation service was tested. Shared English and structured-fact controls are reused, not counted as extra generations.

## Results

| Condition | Qwen3-0.6B strict | Qwen3-1.7B strict |
|---|---:|---:|
| baseline | 0/300 | 37/300 |
| localized_policy | 0/240 | 21/240 |
| structured_facts | 0/60 | 6/60 |
| recovery | 187/300 | 76/300 |

| User language | Qwen3-0.6B strict / fence-only | Qwen3-1.7B strict / fence-only |
|---|---:|---:|
| en | 0/60 / 0/60 | 11/60 / 11/60 |
| es | 0/60 / 0/60 | 11/60 / 11/60 |
| zh-Hans | 0/60 / 0/60 | 4/60 / 4/60 |
| uk | 0/60 / 0/60 | 9/60 / 9/60 |
| ht | 0/60 / 0/60 | 2/60 / 2/60 |

Strict requires one exact-schema JSON call. Fence-only removes just an enclosing Markdown JSON fence; it does not repair arguments or prose. Every recorded call is replayed against the sandbox state.

## Correction by language

| User language | Qwen3-0.6B strict | Qwen3-1.7B strict |
|---|---:|---:|
| en | 58/60 | 10/60 |
| es | 45/60 | 2/60 |
| zh-Hans | 43/60 | 10/60 |
| uk | 39/60 | 38/60 |
| ht | 2/60 | 16/60 |

Correction varies by model and language; the larger model does not uniformly improve it. Draft translations and different conversation histories prevent a general language ranking.

## Diagnostic findings

**Qwen3-0.6B**

- Format: 0/300 baseline answers meet the schema; fence removal adds 0 correct calls.
- Structured facts versus English baseline: 0 control-only successes, 0 baseline-only successes, 0 shared successes and 60 shared failures across 60 matched decisions.
- Localized policy: 0 successes gained and 0 lost across 240 matched decisions. Translation and language mixing remain possible explanations.
- Correction: 187/300 seeded wrong proposals are corrected under strict scoring. This is not recovery from the model's own baseline mistakes.
- Parsed unauthorized mutation attempts: 38; sandbox safeguards block them. Invalid outputs also fail, so this count alone is not a safety score.

**Qwen3-1.7B**

- Format: 278/300 baseline answers meet the schema; fence removal adds 0 correct calls.
- Structured facts versus English baseline: 5 control-only successes, 10 baseline-only successes, 1 shared successes and 44 shared failures across 60 matched decisions.
- Localized policy: 6 successes gained and 11 lost across 240 matched decisions. Translation and language mixing remain possible explanations.
- Correction: 76/300 seeded wrong proposals are corrected under strict scoring. This is not recovery from the model's own baseline mistakes.
- Parsed unauthorized mutation attempts: 55; sandbox safeguards block them. Invalid outputs also fail, so this count alone is not a safety score.

## How to read the evidence

Language-associated differences are leads for independent review. They do not isolate language from translation quality, instruction wording, mixed-language interfaces or model limitations. Strong English/oracle failures weaken a language-only explanation; success after an oracle intervention suggests an interpretation bottleneck but does not uniquely identify its cause.

All tasks withhold approval. The correction condition uses an injected reachable proposal and a scripted user response, and supplies a valid JSON example. Baseline-versus-correction differences cannot separate correction skill from example-driven format adherence or other history effects. This tests bounded tool decisions and controlled correction, not autonomous end-to-end agents, positive consent, cultural competence or real-world harm.

The effective diversity is six template families, not 1,800 independent situations. No confidence intervals, significance, language rankings, equivalence or population-level fairness claims. Two models from one family are a limited replication.

## Original contribution and next test

LocaleSafe contributes authored service scenarios, executable state checks and matched interventions that separate interface, interpretation and workflow outcomes. It does not claim to invent multilingual evaluation or failure decomposition.

Next: independently review translations, add held-out scenarios and positive approval cases, collect genuinely interactive episodes, and replicate with another model family. Cultural context needs separately reviewed cases; script coverage alone does not establish it.

[Raw outputs, source and hashes](../experiments/README.md#latest-matched-workflow-study) · [Frozen protocol and amendments](../experiments/workflow/PROTOCOL.md) · [Execution history](../experiments/workflow/EXECUTION_HISTORY.md) · [Benchmark registry](BENCHMARKS.md)
