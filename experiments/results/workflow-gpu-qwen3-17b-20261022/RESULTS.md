# Qwen/Qwen3-1.7B: language or workflow?

900 real generations. 30 scenarios × five languages, two repeats; shared controls. Free Colab Tesla T4; float16, no quantization. No paid APIs.

## Recorded performance

| Condition | Strict correct | Fence-only correct | Executable | Unauthorized attempts |
|---|---:|---:|---:|---:|
| baseline | 37/300 | 37/300 | 156/300 | 0 |
| localized_policy | 21/240 | 21/240 | 67/240 | 0 |
| recovery | 76/300 | 76/300 | 119/300 | 55 |
| structured_facts | 6/60 | 6/60 | 11/60 | 0 |

| Language | Baseline strict | Localized policy strict | Recovery strict |
|---|---:|---:|---:|
| en | 11/60 | reuse English baseline | 10/60 |
| es | 11/60 | 13/60 | 2/60 |
| ht | 2/60 | 0/60 | 16/60 |
| uk | 9/60 | 0/60 | 38/60 |
| zh-Hans | 4/60 | 8/60 | 10/60 |

## Matched English restatement control

English baseline versus target-language baseline on identical scenario/repeat. The English request is a parallel authored restatement, not an output from a translation system.

| Target | Both correct | Both wrong | English only | Target only |
|---|---:|---:|---:|---:|
| es | 7 | 45 | 4 | 4 |
| ht | 2 | 49 | 9 | 0 |
| uk | 5 | 45 | 6 | 4 |
| zh-Hans | 4 | 49 | 7 | 0 |

## Scope

Each generated JSON call is executed in a deterministic sandbox. Correct calls and final states are checked separately from schema validity and execution. Canonical calls pass all controls; reachable wrong proposals fail task success.

Recovery starts with an injected wrong proposal and a scripted rejection. It also exposes a valid JSON example, so improvement over baseline cannot be attributed uniquely to correction ability. It does not measure recovery from the model's own mistakes or full autonomous conversations. Every task withholds approval: no positive-consent competence is measured.

Structured facts deliberately remove interpretation work; they are canonical authored facts, not model-extracted facts. English controls are reused across languages and are not additional generations. Tool schemas and slot/day IDs stay in English/invariant form when policy language changes.

Draft translations, six template families, related models, quantization and small samples limit attribution. No human-reviewed translation rescue, held-out validation, significance, language ranking or real-world harm claim. Differences are diagnostic leads; zero differences do not establish equivalence.

Exact prompts, raw outputs, seeds, execution states and failures: attempts.jsonl. Full paired contrasts, error types and per-family scores: summary.json. Protocol was frozen before task collection.
