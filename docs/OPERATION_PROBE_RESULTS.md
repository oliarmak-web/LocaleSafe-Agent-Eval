# Requested-operation probe: results

336 greedy calls; the same 56 draft cases, each tested under all six A/B/C option orders. This identifies wait/propose/commit only; it does not execute an action or test exact arguments, authorization or final state.

| Pattern | Valid letters | Correct choices | Cases correct under all six orders | Order-sensitive cases | Parent full-action score |
|---|---:|---:|---:|---:|---:|
| en-en | 48/48 | 24/48 | 0/8 | 8/8 | 8/8 |
| es-es | 48/48 | 22/48 | 0/8 | 8/8 | 8/8 |
| en-es | 48/48 | 20/48 | 0/8 | 8/8 | 8/8 |
| es-en | 48/48 | 23/48 | 0/8 | 8/8 | 8/8 |
| hi-hi | 48/48 | 21/48 | 0/8 | 8/8 | 4/8 |
| en-hi | 48/48 | 21/48 | 0/8 | 8/8 | 6/8 |
| hi-en | 48/48 | 23/48 | 0/8 | 8/8 | 8/8 |

All six permutations give each reference answer letter twice per case. The 48 choices per language pattern are repeated measurements on eight situation/variant rows, not 48 independent situations.

The parent action score includes target, value and version; this probe changes the prompt and output task. The narrower choice score cannot replace the full-action score or establish language comprehension.

## Accuracy by correct answer position

| Pattern | A | B | C |
|---|---:|---:|---:|
| en-en | 0/16 | 16/16 | 8/16 |
| es-es | 0/16 | 16/16 | 6/16 |
| en-es | 0/16 | 16/16 | 4/16 |
| es-en | 0/16 | 16/16 | 7/16 |
| hi-hi | 0/16 | 14/16 | 7/16 |
| en-hi | 0/16 | 12/16 | 9/16 |
| hi-en | 0/16 | 16/16 | 7/16 |

Designed after inspecting parent errors. Hindi and Spanish text lack independent review; there is no held-out evaluation or significance claim. See the machine-readable summary for per-order counts, selected-letter counts and individual changed-task comparisons.
