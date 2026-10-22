# What the experiments show

## Latest: language, interface, and model interact

The [two-model workflow study](WORKFLOW_STUDY.md) recorded 1,800 decisions across five languages, using matched requests, localized policies, canonical structured facts and seeded correction interactions.

- **Schema validity hides errors.** Qwen3-1.7B produced 278/300 valid baseline calls; only 37/300 were correct. Wrong arguments accounted for 239 failures.
- **Removing interpretation did not fix action generation.** Its English baseline scored 11/60. Canonical facts scored 6/60, with 44 matched failures shared by both conditions. This weakens an explanation based only on understanding non-English requests.
- **Language sensitivity is configuration-specific.** Qwen3-0.6B corrected 58/60 English proposals and 2/60 Haitian Creole proposals. Qwen3-1.7B scored 10/60 and 16/60 respectively. Ukrainian correction scores were 39/60 and 38/60. These patterns warrant review, not a general language ranking.
- **Translated policies were not a consistent fix.** On the larger model they gained six matched successes and lost eleven across 240 decisions.
- **Conversation history matters.** The small model failed every strict baseline call but corrected 187/300 seeded proposals. That condition also supplies a JSON example; it does not isolate recovery skill from format priming.

**Conclusion:** multilingual evaluation is useful for finding configuration-specific failures. These runs do not establish that language is the main cause. Better English competence, independently reviewed translations and held-out interactive tasks are needed before a causal claim.

## Earlier: five languages, no answer options

80 new generations tested English, Spanish, Simplified Chinese, Ukrainian, and Haitian Creole. Each language had eight date requests and two repeats. Strict interpretation: English 6/16, Spanish 4/16, Chinese 5/16, Ukrainian 5/16, Haitian Creole 4/16.

**Shared weakness:** 36/80 answers asked for clarification unnecessarily. Explicit month-name requests were correct in 0/10 attempts, including English. This small model struggles with the task beyond a simple non-English disadvantage.

**Different failure types:** Ukrainian had 9/16 invalid scalar answers, versus 2–3/16 in the other languages. That is a useful review target, not proof of a general language gap. The translations are draft and the sample is tiny.

**A workflow defect mattered:** the scripted clarification reply used a U.S. date in GB cases. This caused 12 of 13 original wrong sandbox commits. Replaying identical answers with a corrected reply reduces wrong commits to 1 and increases completion from 48/80 to 60/80. Interpretation stays 24/80. Original outputs and scores are preserved; this repair is post-hoc.

Completion can improve while understanding does not: the scripted reply supplies missing information. The fixed adapter handles confirmation; this is not an autonomous-agent or real-user experiment. No real appointments changed.

[Full results and raw evidence](../experiments/results/direct-five-language-20261021/INSIGHTS.md).

## 1. Formatting can masquerade as a language failure

The first pilot produced 92/108 Markdown-wrapped answers that failed strict JSON parsing. Removing only the wrappers changed scores substantially. Those failures cannot be presented as evidence of language misunderstanding.

## 2. The controlled probe did not show a clear one-sided language gap

With formatting fixed, English was correct in 69/216 sampled choices; Spanish in 70/216. Matched contrasts: 14 English-only successes, 15 Spanish-only successes, 132 shared failures, 55 shared successes.

These are repeated choices on two date families—not 216 independent situations. Near-equal scores do not prove language equivalence.

## 3. Answer position is the dominant warning

The model selected A in 98/108 English workflow choices, although each correct plan occupied A, B, and C equally often. Only 44/108 workflow choices were correct. This is a plan-selection failure, but label bias prevents isolating workflow understanding as its cause.

Canonical correct choices pass all 30 simulator controls. No executor defect was detected in those controls; this does not validate production software.

## Decision

**Do not claim language bias from these runs.** We cross-checked direct answers and found shared interpretation problems, output-format differences, and a consequential fixture defect. Next: independently review translations, replicate with a stronger model, and add held-out families plus interactive confirmation before studying language effects.

[Controlled results](../experiments/results/attribution-20261021/INSIGHTS.md) · [Protocol](../experiments/attribution/PROTOCOL.md) · [Original pilot](../experiments/results/qwen3-06b-20261021/RESULTS.md)
