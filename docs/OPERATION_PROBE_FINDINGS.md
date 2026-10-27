# A simpler answer format introduced answer-position bias

**336 archived Qwen3-4B calls, October 27, 2026.** Exploratory diagnostic designed after inspecting the Hindi-pair errors. The same 56 draft rows were tested under all six orders of wait/propose/commit assigned to A/B/C. No new independent task families or language reviews.

## What happened?

Every response was a valid letter, but **the model never selected A in any of the 336 calls**. In English-only cases, it selected B 36 times and C 12 times. English accuracy was 24/48 choices, even though the parent full-action task scored 8/8 greedy English actions.

When the correct English answer was A, accuracy was **0/16**; when it was B, **16/16**; when it was C, **8/16**. Every situation/variant in every language pattern changed correctness across option orderings. No case was correct under all six permutations.

This is an answer-order sensitivity result under this prompt setup. It is not evidence that the user requested different operations across translations. Each case's history was unchanged while the answer mapping was permuted.

## What this means for language evaluation

Removing the JSON tool-call requirement did not produce a clean comprehension test. The new prompt asked a different, narrower task and introduced a strong letter-position effect. A single favorable ordering could make the model look more capable than the complete counterbalanced result supports.

The language-pattern totals ranged from 20/48 to 24/48 correct, but the strong English position effect and zero all-order consistency prevent a useful language ranking. These are six repeated tests on eight situation/variant rows per pattern, not 48 independent situations. The probe also omits record/value/version and authorization checks, so its score cannot replace the parent action score.

**Practical use:** counterbalance multiple-choice labels before treating them as evidence of language understanding. Report validity, correctness, position effects and consistency separately. A format can be perfectly valid and still provide an unreliable evaluation signal.

This negative result is preserved alongside the original Hindi-condition failures and the longer workflow's failed English screen. No prompt was revised after these outputs to rescue the score.

## Reproduce

```sh
python -m experiments.summarize_operation_probe experiments/results/operation-probe-qwen3-4b-20261027 --output-dir reports/my-operation-analysis
```

Python 3.11+, no model download or API key for replay. Choose a new directory. The audit also verifies the parent Hindi-pair archive. [Tables](OPERATION_PROBE_RESULTS.md) · [Protocol](../experiments/operation-probe/PROTOCOL.md) · [Execution history](../experiments/operation-probe/EXECUTION_HISTORY.md) · [Machine-readable results](../experiments/analysis/operation-probe/summary.json).
