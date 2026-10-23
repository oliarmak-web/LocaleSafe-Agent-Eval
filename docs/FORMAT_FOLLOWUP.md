# JSON-example prompt intervention

Exploratory development-only follow-up. Original scores remain unchanged. No output repair or constrained decoding.

| Model | Evidence | Prompt arm | Valid actions | Correct actions | Unauthorized attempts | Token-limit hits |
|---|---|---|---:|---:|---:|---:|
| mistralai/Mistral-7B-Instruct-v0.3 | full_history | baseline_repeat | 0/32 | 0/32 | 0 | 0 |
| mistralai/Mistral-7B-Instruct-v0.3 | full_history | json_examples | 32/32 | 32/32 | 0 | 0 |
| mistralai/Mistral-7B-Instruct-v0.3 | oracle_record | baseline_repeat | 12/32 | 4/32 | 8 | 0 |
| mistralai/Mistral-7B-Instruct-v0.3 | oracle_record | json_examples | 32/32 | 16/32 | 16 | 0 |
| microsoft/Phi-4-mini-instruct | full_history | baseline_repeat | 16/32 | 15/32 | 1 | 0 |
| microsoft/Phi-4-mini-instruct | full_history | json_examples | 32/32 | 28/32 | 0 | 0 |
| microsoft/Phi-4-mini-instruct | oracle_record | baseline_repeat | 32/32 | 32/32 | 0 | 0 |
| microsoft/Phi-4-mini-instruct | oracle_record | json_examples | 23/32 | 23/32 | 0 | 0 |

mistralai/Mistral-7B-Instruct-v0.3: 44 paired improvements, 0 regressions. Baseline exact-text agreement: 64/64.


microsoft/Phi-4-mini-instruct: 13 paired improvements, 9 regressions. Baseline exact-text agreement: 64/64.

Small, previously inspected draft cases cannot establish language bias, a production fix or a stable model ranking.
Unauthorized attempts require valid commit outputs; invalid commands are failures, not evidence of safe intent.
Baseline repetitions and intervention calls are paired observations, not new independent situations.

[Protocol](../experiments/format-followup/PROTOCOL.md).
