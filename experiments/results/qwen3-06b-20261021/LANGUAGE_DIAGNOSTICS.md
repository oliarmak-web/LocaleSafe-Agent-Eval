# Language versus workflow: exploratory diagnostics

These comparisons do not establish a causal language effect. Six scenario families, draft translations, one model, and one generation per item cannot disentangle language, translation, phrasing, sampling, and prompt sensitivity.

The strict analysis measures the complete output contract. Fence-only parsing is a post-hoc diagnostic on the exact same generations. No model decisions or arguments are changed. Decision/tool errors below are conditional on parseable outputs; missing/unparseable decisions are unknown, not inferred errors. Error categories overlap.

## baseline / strict

| Language | All | Parseable | Format failures | Decision errors / parseable | Tool errors / parseable |
|---|---:|---:|---:|---:|---:|
| ar | 6 | 4 | 2 | 1/4 | 0/4 |
| en | 6 | 0 | 6 | 0/0 | 0/0 |
| es | 6 | 1 | 5 | 0/1 | 0/1 |
| ht | 6 | 0 | 6 | 0/0 | 0/0 |
| ko | 6 | 1 | 5 | 0/1 | 0/1 |
| tl | 6 | 1 | 5 | 0/1 | 0/1 |
| uk | 6 | 3 | 3 | 2/3 | 1/3 |
| vi | 6 | 2 | 4 | 1/2 | 1/2 |
| zh-Hans | 6 | 1 | 5 | 1/1 | 0/1 |

Paired complete-task outcomes versus the same English scenario:

| Language | Both pass | Both fail | English pass / other fail | English fail / other pass | Pairs with unparseable output |
|---|---:|---:|---:|---:|---:|
| ar | 0 | 3 | 0 | 3 | 6 |
| es | 0 | 5 | 0 | 1 | 6 |
| ht | 0 | 6 | 0 | 0 | 6 |
| ko | 0 | 5 | 0 | 1 | 6 |
| tl | 0 | 5 | 0 | 1 | 6 |
| uk | 0 | 5 | 0 | 1 | 6 |
| vi | 0 | 5 | 0 | 1 | 6 |
| zh-Hans | 0 | 6 | 0 | 0 | 6 |

Unparseable-pair counts overlap the pass/fail columns. English-pass/other-fail is a candidate language-associated counterexample; inspect the raw case and translation before attribution. Both-fail is a shared failure, not proof of a particular workflow bug. JSON includes decision-only paired discordances and their parseable-pair denominator.

## baseline / fence_only_posthoc

| Language | All | Parseable | Format failures | Decision errors / parseable | Tool errors / parseable |
|---|---:|---:|---:|---:|---:|
| ar | 6 | 6 | 0 | 2/6 | 1/6 |
| en | 6 | 6 | 0 | 2/6 | 1/6 |
| es | 6 | 6 | 0 | 2/6 | 1/6 |
| ht | 6 | 6 | 0 | 3/6 | 3/6 |
| ko | 6 | 6 | 0 | 2/6 | 1/6 |
| tl | 6 | 6 | 0 | 3/6 | 1/6 |
| uk | 6 | 6 | 0 | 2/6 | 1/6 |
| vi | 6 | 6 | 0 | 2/6 | 1/6 |
| zh-Hans | 6 | 6 | 0 | 2/6 | 1/6 |

Paired complete-task outcomes versus the same English scenario:

| Language | Both pass | Both fail | English pass / other fail | English fail / other pass | Pairs with unparseable output |
|---|---:|---:|---:|---:|---:|
| ar | 4 | 2 | 0 | 0 | 0 |
| es | 4 | 2 | 0 | 0 | 0 |
| ht | 3 | 2 | 1 | 0 | 0 |
| ko | 4 | 2 | 0 | 0 | 0 |
| tl | 3 | 2 | 1 | 0 | 0 |
| uk | 4 | 2 | 0 | 0 | 0 |
| vi | 4 | 2 | 0 | 0 | 0 |
| zh-Hans | 4 | 2 | 0 | 0 | 0 |

Unparseable-pair counts overlap the pass/fail columns. English-pass/other-fail is a candidate language-associated counterexample; inspect the raw case and translation before attribution. Both-fail is a shared failure, not proof of a particular workflow bug. JSON includes decision-only paired discordances and their parseable-pair denominator.

## check / strict

| Language | All | Parseable | Format failures | Decision errors / parseable | Tool errors / parseable |
|---|---:|---:|---:|---:|---:|
| ar | 6 | 3 | 3 | 2/3 | 1/3 |
| en | 6 | 0 | 6 | 0/0 | 0/0 |
| es | 6 | 0 | 6 | 0/0 | 0/0 |
| ht | 6 | 0 | 6 | 0/0 | 0/0 |
| ko | 6 | 0 | 6 | 0/0 | 0/0 |
| tl | 6 | 0 | 6 | 0/0 | 0/0 |
| uk | 6 | 0 | 6 | 0/0 | 0/0 |
| vi | 6 | 0 | 6 | 0/0 | 0/0 |
| zh-Hans | 6 | 0 | 6 | 0/0 | 0/0 |

Paired complete-task outcomes versus the same English scenario:

| Language | Both pass | Both fail | English pass / other fail | English fail / other pass | Pairs with unparseable output |
|---|---:|---:|---:|---:|---:|
| ar | 0 | 5 | 0 | 1 | 6 |
| es | 0 | 6 | 0 | 0 | 6 |
| ht | 0 | 6 | 0 | 0 | 6 |
| ko | 0 | 6 | 0 | 0 | 6 |
| tl | 0 | 6 | 0 | 0 | 6 |
| uk | 0 | 6 | 0 | 0 | 6 |
| vi | 0 | 6 | 0 | 0 | 6 |
| zh-Hans | 0 | 6 | 0 | 0 | 6 |

Unparseable-pair counts overlap the pass/fail columns. English-pass/other-fail is a candidate language-associated counterexample; inspect the raw case and translation before attribution. Both-fail is a shared failure, not proof of a particular workflow bug. JSON includes decision-only paired discordances and their parseable-pair denominator.

## check / fence_only_posthoc

| Language | All | Parseable | Format failures | Decision errors / parseable | Tool errors / parseable |
|---|---:|---:|---:|---:|---:|
| ar | 6 | 6 | 0 | 3/6 | 1/6 |
| en | 6 | 6 | 0 | 2/6 | 1/6 |
| es | 6 | 6 | 0 | 2/6 | 1/6 |
| ht | 6 | 6 | 0 | 3/6 | 2/6 |
| ko | 6 | 6 | 0 | 2/6 | 1/6 |
| tl | 6 | 6 | 0 | 4/6 | 2/6 |
| uk | 6 | 6 | 0 | 3/6 | 2/6 |
| vi | 6 | 6 | 0 | 2/6 | 1/6 |
| zh-Hans | 6 | 6 | 0 | 2/6 | 1/6 |

Paired complete-task outcomes versus the same English scenario:

| Language | Both pass | Both fail | English pass / other fail | English fail / other pass | Pairs with unparseable output |
|---|---:|---:|---:|---:|---:|
| ar | 3 | 2 | 1 | 0 | 0 |
| es | 4 | 2 | 0 | 0 | 0 |
| ht | 3 | 2 | 1 | 0 | 0 |
| ko | 4 | 2 | 0 | 0 | 0 |
| tl | 2 | 2 | 2 | 0 | 0 |
| uk | 3 | 2 | 1 | 0 | 0 |
| vi | 4 | 2 | 0 | 0 | 0 |
| zh-Hans | 4 | 2 | 0 | 0 | 0 |

Unparseable-pair counts overlap the pass/fail columns. English-pass/other-fail is a candidate language-associated counterexample; inspect the raw case and translation before attribution. Both-fail is a shared failure, not proof of a particular workflow bug. JSON includes decision-only paired discordances and their parseable-pair denominator.

## Benchmarks and next controls

See `docs/BENCHMARKS.md` for the exact custom-suite status, external benchmarks not yet run, and the next controlled study design. Add reviewed parallel inputs, English paraphrase controls, repeated generations, a canonical tool-simulator control, and constrained-output comparisons before attributing an effect to language.
