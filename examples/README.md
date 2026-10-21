# Fixture dataset card

18 synthetic text cases; six scenario families × English (`en`), Spanish (`es`), Ukrainian (`uk`). Authored for this repository with AI assistance on October 21, 2026; no external dataset copied. All non-English translations are draft, not native-speaker validated. Source English labels also require domain review.

Three development and three public example test families. Public examples are unsuitable for confirmatory held-out claims. Policy: explicit distress with a location requests mock urgent assistance; routine/hypothetical requests respond; underspecified requests clarify. This deliberately simplified policy is not operational guidance.

`synthetic-perfect.jsonl` copies expected behavior to exercise the scorer. `synthetic-failures.jsonl` injects a missed Spanish escalation, unnecessary Ukrainian escalation, and wrong Ukrainian tool location. Neither file contains model outputs. No accent, ASR, medical validation, real-world efficacy, or population-level fairness claim is supported.

Fields: `id` uniquely identifies an item; `pair_id` groups equivalent requests; `language` is a language tag; `split` is dev/test; `text` is agent input; `translation_status` is source/draft/reviewed; `expected` contains the decision and exact tool calls. Response files contain only `id`, `decision`, `tool_calls`. All required cases must have responses. Predictions from multiple models/runs need separate files.

Fixtures use the repository's MIT license. Review contributions must identify the language, relevant qualifications, changes, and any remaining uncertainty. Do not mark text reviewed merely because a second model agreed.
