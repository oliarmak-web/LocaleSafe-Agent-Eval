# Language or workflow? Controlled results

Model: `Qwen/Qwen3-0.6B`. 30 tasks; 180 forward passes; 540 sampled choices. No paid API.

**Scope:** closed-choice recognition, not a live agent. Formatting is fixed by design. Translations are draft. Repeated choices are not independent tasks.

**Lead finding:** strong answer-position sensitivity limits attribution. The workflow probe chose A in 98/108 draws despite balanced correct-answer positions. Check the response method before attributing failures to language or workflow comprehension.

## Interpretation

| Language | Items | Correct / sampled choices | Mean probability on correct option |
|---|---:|---:|---:|
| en | 12 | 69/216 | 35.7% |
| es | 12 | 70/216 | 34.4% |

Probabilities are conditional on the three offered tokens, not calibrated confidence or free-form accuracy. Uniform-choice reference: 33.3%; no inferential test is claimed.

| Explicit locale | Correct / choices | Mean correct-option probability |
|---|---:|---:|
| US | 69/144 | 46.0% |
| GB | 40/144 | 31.0% |
| unspecified | 30/144 | 28.1% |

Matched draws: English-only correct **14**; Spanish-only correct **15**; both wrong **132**; both correct **55**.

| Phrasing control | P0-only correct | P1-only correct | Mean P0−P1 probability |
|---|---:|---:|---:|
| en | 2 | 3 | 0.6% |
| es | 17 | 7 | 6.0% |

## Workflow with known facts

English-only controls remove translation/date extraction. The model selects a plan; the sandbox executes it.

| Rule | Correct / choices | Mean correct-option probability |
|---|---:|---:|
| confirmation | 6/18 | 33.4% |
| denial | 5/18 | 33.4% |
| edit | 6/18 | 33.3% |
| duplicate | 6/18 | 33.3% |
| handoff | 15/18 | 86.5% |
| clarification | 6/18 | 33.5% |

Workflow total: **44/108** choices correct. Canonical correct actions pass **30/30** simulator controls.

## Answer-position control

Mean probability on the correct option, grouped by its label. Large differences indicate position sensitivity even though aggregate orders are balanced.

| Probe | Correct at A | Correct at B | Correct at C |
|---|---:|---:|---:|
| interpretation | 74.8% | 24.1% | 6.3% |
| workflow | 99.6% | 10.5% | 16.6% |

## What this establishes

- Format errors cannot explain failures in this constrained probe.
- English-only plan selection failed in 64/108 sampled choices; translation is not required for those failures. Label bias prevents attributing these errors specifically to workflow understanding.
- Language and phrasing contrasts identify candidates for review, not causal population effects.
- Perfect canonical replay validates these controls, not production workflow reliability.

## Limits

Two date families; six workflow tasks; one small model; draft translations; offered answers; no interactive planning. Difficulty differs between probes, so their error rates cannot allocate a single causal share to language versus workflow. No significance/equivalence claims. Next: human review, held-out families, more models, free-form and interactive replications.

Evidence: `tasks.jsonl`, exact prompts/probabilities/seeds/scores in `attempts.jsonl`, settings/hashes in `manifest.json`, position diagnostics in `summary.json`. The protocol was frozen before collection; this descriptive analysis was written during the run.
