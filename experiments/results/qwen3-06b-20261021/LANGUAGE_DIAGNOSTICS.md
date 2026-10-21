# Language versus workflow: exploratory diagnostics

Exploratory: six families, draft translations, one model, one draw per condition. No causal language-effect claim.

Strict = output contract. Fence-only = post-hoc wrapper removal on the same answers. Semantic errors use parseable outputs only; unparseable decisions remain unknown. Categories overlap.

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

Unparseable pairs overlap pass/fail counts. Disagreements need review; shared failures do not prove a workflow cause. Decision-only contrasts are in JSON.

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

Unparseable pairs overlap pass/fail counts. Disagreements need review; shared failures do not prove a workflow cause. Decision-only contrasts are in JSON.

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

Unparseable pairs overlap pass/fail counts. Disagreements need review; shared failures do not prove a workflow cause. Decision-only contrasts are in JSON.

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

Unparseable pairs overlap pass/fail counts. Disagreements need review; shared failures do not prove a workflow cause. Decision-only contrasts are in JSON.

## Benchmarks and next controls

Next: reviewed translations, English paraphrases, repeat runs, executor controls, and fixed output handling. External benchmarks have not been run.
