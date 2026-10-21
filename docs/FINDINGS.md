# What the experiments show

## 1. Formatting can masquerade as a language failure

The first pilot produced 92/108 Markdown-wrapped answers that failed strict JSON parsing. Removing only the wrappers changed scores substantially. Those failures cannot be presented as evidence of language misunderstanding.

## 2. The controlled probe did not show a clear one-sided language gap

With formatting fixed, English was correct in 69/216 sampled choices; Spanish in 70/216. Matched contrasts: 14 English-only successes, 15 Spanish-only successes, 132 shared failures, 55 shared successes.

These are repeated choices on two date families—not 216 independent situations. Near-equal scores do not prove language equivalence.

## 3. Answer position is the dominant warning

The model selected A in 98/108 English workflow choices, although each correct plan occupied A, B, and C equally often. Only 44/108 workflow choices were correct. This is a plan-selection failure, but label bias prevents isolating workflow understanding as its cause.

Canonical correct choices pass all 30 simulator controls. No executor defect was detected in those controls; this does not validate production software.

## Decision

**Do not claim language bias from these runs.** The evidence exposes formatting and choice-position confounds. Next: cross-check the response method and a stronger model, independently review translations, and add new held-out families before studying language effects.

[Controlled results](../experiments/results/attribution-20261021/INSIGHTS.md) · [Protocol](../experiments/attribution/PROTOCOL.md) · [Original pilot](../experiments/results/qwen3-06b-20261021/RESULTS.md)
