# The longer workflow broke English too

**864 archived Qwen3-4B calls, October 27, 2026.** Four-turn exploratory text follow-up on four draft permission-change templates, with no independent language review or held-out evaluation.

## What we changed

Every conversation contained an approval, a neutral reminder, a critical change of instruction and another neutral reminder. English-only, Spanish-only and Hindi-only baselines were compared with switches from English before, at or after the critical instruction. Moving the switch also changed the number of partner-language turns; it did not isolate switch location alone.

## The English screen failed

English full-history correctness fell to **4/8**, below the frozen 7/8 screen; reference-record actions remained **8/8**. The four wrong English actions chose the correct operation, record and value but used an older permission version.

The harness increments its version for every event, including a neutral reminder that preserves approval. It therefore required version 4 even though the substantive correction appeared at turn 3. This synthetic bookkeeping rule is a material part of what failed. It is not evidence that English users revoked permission, that real customers were harmed or that language caused the failure.

**We cannot use this experiment to claim a reliable language-switch-position effect.** Hindi-only and English→Hindi layouts also had low strict scores, but the failed English baseline and artificial version contract limit interpretation. All results remain archived; none were discarded or repaired to pass the screen.

## Separating the error types

A clearly marked **post-hoc diagnostic** checked operation, record and value while excluding the permission-version field. English matched those fields in 8/8 greedy cases despite scoring 4/8 on the unchanged full contract. This diagnostic does not turn a rejected command into an authorized action or change the failed screen.

Across all three decoding profiles, full-history actors made **101/216 contract-rejected commit attempts**. Of these, **99 had the correct requested operation, record and value but a stale version**; two had other mismatches. The separate guard blocked all 101. Reference-record and generated-record conditions had no rejected commit attempts, but generated-record greedy task correctness was only 2/8 in every layout: low unsafe-attempt counts do not imply successful completion.

All nine layouts shared identical reference-record prompts within each situation. Their greedy replies also matched exactly within each of the eight situation/variant blocks, with 8/8 correctness per layout. This confirms that the representation control behaved consistently in this run; it does not validate automatic record generation.

## Why this is useful

Before blaming a language, inspect the evaluator's own state and version rules. A benchmark can flag a command because its bookkeeping is wrong even when the model selected the requested operation and target correctly. Production approval versions and conversation sequence numbers need explicit, separately defined semantics; this study does not validate a production design for either.

The frozen primary scores are preserved. A future study that separates event sequence from approval version must use a new protocol and new artifacts, rather than rewriting this run. The separate [operation probe](../experiments/operation-probe/PROTOCOL.md) tests a narrower question without tool-call arguments or version construction.

## Reproduce

```sh
python -m experiments.summarize_switch_boundary experiments/results/switch-boundary-qwen3-4b-20261027 --output-dir reports/my-boundary-analysis
```

Python 3.11+, no model download or API keys for replay. Choose a new directory. [Tables](SWITCH_BOUNDARY_RESULTS.md) · [Protocol](../experiments/switch-boundary/PROTOCOL.md) · [Execution history](../experiments/switch-boundary/EXECUTION_HISTORY.md) · [Machine-readable results](../experiments/analysis/switch-boundary/summary.json).
