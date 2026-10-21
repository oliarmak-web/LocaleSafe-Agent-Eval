# Direct-answer multilingual probe

80 real local generations · Qwen3-0.6B · 40 draft items · two repeats · no paid APIs.

No answer options were supplied. The model returned a date or CLARIFY; a fixed adapter replayed that answer in the appointment sandbox.

| Language | Strict correct | Fence-only correct | Strict parsed | Original sandbox wrong commits |
|---|---:|---:|---:|---:|
| en | 6/16 | 6/16 | 13/16 | 3 |
| es | 4/16 | 4/16 | 14/16 | 3 |
| ht | 4/16 | 4/16 | 13/16 | 4 |
| uk | 5/16 | 5/16 | 7/16 | 0 |
| zh-Hans | 5/16 | 5/16 | 14/16 | 3 |

## Controls

| Date form | Strict correct | Parsed | Unnecessary clarification |
|---|---:|---:|---:|
| iso | 2/10 | 10 | 8 |
| month_name | 0/10 | 10 | 10 |
| numeric | 22/60 | 41 | 18 |

Numeric-date interpretation by explicit locale:

- US: 3/20 correct.
- GB: 0/20 correct.
- None: 19/20 correct.

## A workflow defect changed the outcome

The scripted clarification reply used a U.S. date even for GB requests. That fixture defect accounts for 12 of 13 original wrong commits. It is not a model-language finding.

Post-hoc replay sets that reply to the case's intended date, without rerunning or changing model answers. Wrong commits fall from 13 to 1; completion rises from 48/80 to 60/80. Interpretation remains 24/80. This isolates a sandbox-script effect on these recorded outputs, not an improvement in the model.

The corrected reply is an oracle control, not a prediction of what a real user would say. Original data and scores remain unchanged.

## What this establishes

This cross-check removes the earlier A/B/C answer-position confound. English failures and explicit-date controls test whether a language-only explanation is plausible. They do not isolate a causal language effect.

Interpretation and completion differ: an unnecessary clarification can recover through the scripted reply. A wrong commit means a wrong date reached the sandbox after scripted approval; no real appointment was changed.

Workflow confirmation is supplied by code. These results measure interpretation plus a fixed adapter, not autonomous planning, real user behavior, or operational harm.

Draft translations, one small model, eight items per language, and two stochastic repeats cannot support language rankings, equivalence, significance, or cultural competence claims. Repeats are not independent scenarios.

Next: independent translation review, new held-out situations, a stronger model, and interactive confirmation where the user can reject an incorrect date.

See summary.json for paired English contrasts, per-language controls, and strict versus uniform fence-only scoring. Raw outputs and exact prompts are in attempts.jsonl.
