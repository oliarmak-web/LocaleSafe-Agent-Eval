# Qwen/Qwen3-0.6B: language or workflow?

900 real generations. 30 scenarios × five languages, two repeats; shared controls. Free Colab Tesla T4; float16, no quantization. No paid APIs.

## Recorded performance

| Condition | Strict correct | Fence-only correct | Executable | Unauthorized attempts |
|---|---:|---:|---:|---:|
| baseline | 0/300 | 0/300 | 0/300 | 0 |
| localized_policy | 0/240 | 6/240 | 0/240 | 0 |
| recovery | 187/300 | 187/300 | 259/300 | 38 |
| structured_facts | 0/60 | 0/60 | 0/60 | 0 |

| Language | Baseline strict | Localized policy strict | Recovery strict |
|---|---:|---:|---:|
| en | 0/60 | reuse English baseline | 58/60 |
| es | 0/60 | 0/60 | 45/60 |
| ht | 0/60 | 0/60 | 2/60 |
| uk | 0/60 | 0/60 | 39/60 |
| zh-Hans | 0/60 | 0/60 | 43/60 |

## Matched English restatement control

English baseline versus target-language baseline on identical scenario/repeat. The English request is a parallel authored restatement, not an output from a translation system.

| Target | Both correct | Both wrong | English only | Target only |
|---|---:|---:|---:|---:|
| es | 0 | 60 | 0 | 0 |
| ht | 0 | 60 | 0 | 0 |
| uk | 0 | 60 | 0 | 0 |
| zh-Hans | 0 | 60 | 0 | 0 |

## Scope

Each generated JSON call is executed in a deterministic sandbox. Correct calls and final states are checked separately from schema validity and execution. Canonical calls pass all controls; reachable wrong proposals fail task success.

Recovery starts with an injected wrong proposal and a scripted rejection. It also exposes a valid JSON example, so improvement over baseline cannot be attributed uniquely to correction ability. It does not measure recovery from the model's own mistakes or full autonomous conversations. Every task withholds approval: no positive-consent competence is measured.

Structured facts deliberately remove interpretation work; they are canonical authored facts, not model-extracted facts. English controls are reused across languages and are not additional generations. Tool schemas and slot/day IDs stay in English/invariant form when policy language changes.

Draft translations, six template families, related models, quantization and small samples limit attribution. No human-reviewed translation rescue, held-out validation, significance, language ranking or real-world harm claim. Differences are diagnostic leads; zero differences do not establish equivalence.

Exact prompts, raw outputs, seeds, execution states and failures: attempts.jsonl. Full paired contrasts, error types and per-family scores: summary.json. Protocol was frozen before task collection.
