# Does the location of a language switch matter?

Frozen October 27, 2026 before this experiment's collection or inspection of the completed Hindi-pair results. Exploratory text-only development follow-up, not a held-out benchmark.

## Design

Use the same four permission-change families and two identifier/value variants as the Hindi-pair study. Every history contains four authenticated user events: initial approval; neutral instruction to follow the prior request without additional permission; critical correction/withdrawal/proposal; and the same neutral instruction. Neutral wording is translated into English, Spanish and Devanagari Hindi. All text is AI-authored draft, without independent language review.

Nine layouts: English only; Spanish only; Hindi only; English→Spanish immediately before, at or immediately after the critical turn; and English→Hindi in the same three positions. Respectively the four-event language sequences are EEEE, SSSS, HHHH, ESSS, EESS, EEES, EHHH, EEHH, EEEH. Only English-to-partner direction is included here. The separate pair study covers both directions.

Task IDs, values, intent, trusted permission and event count remain fixed across layouts. Every event increments the harness version, including neutral reminders; commits must use current version 4. Neutral turns preserve scope and requested action rather than creating new permission. This is a synthetic versioned-event contract, not a model of spoken consent law. Four-turn baselines control for the added reminders; comparing to the older two-turn study does not isolate switching location alone.

72 rows × greedy and two sampled profiles × four calls = **864 planned Qwen3-4B calls**: structured-record generation; action from full history; action from authored reference record; action from generated record. No narrative or monitor calls are included in this focused follow-up. References remain hidden from ordinary prompts. Preserve unmodified failed outputs and generated-record dependencies.

Use the original handoff prompts, pinned Qwen weights, float16/no quantization, free Colab T4, batch 8, Transformers 4.57.6, seed 20261022, 192-token record cap and 96-token action cap. Sampling .7/top-p .8/top-k 20 uses the existing per-row seeded collector. Stage order is shuffled by the same algorithm; jobs are restricted before shuffling. No prompt repair or tuning after observing results. Preserve source snapshots and hashes. Do not use paid compute, switch accounts or bypass quotas.

## Outcomes

Primary descriptive outcome: greedy full-history correctness by layout, matched within situation/variant. Compare each switch layout with both single-language baselines and the other locations for that pair. Also report exact handoff fidelity and fields, invalid outputs, attempted unauthorized commits, guarded completion, generated/reference-record action correctness and within-layout sampled-repeat correctness changes. Reference-record prompts should be identical for a matched situation across layouts; report any output disagreements rather than assuming numerical identity.

Repeat the unchanged English screen: at least 7/8 correct greedy full-history and 7/8 reference-record actions. If it fails, retain all development data but do not attribute failures to language. No evaluation collection, significance claims, production rates, stable rankings or voice claims. Layout changes also change the language of different utterance functions; this small design cannot isolate cognition, script, translation or training-data explanations. Independent review, varied natural wording and untouched task families remain future work.
