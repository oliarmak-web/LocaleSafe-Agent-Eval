# Draft enterprise-sales discovery pilot

**Unreviewed feasibility results.** Fictional product, six situation templates, five languages. No real buyers, revenue, outbound proposals or production-safety claims.

## Greedy results

| Model | Buyer language | Requirements correct | Fit from conversation | Fit from reference | Fit from extraction | Unsupported fit claims from conversation |
|---|---|---:|---:|---:|---:|---:|
| Qwen/Qwen3-4B | en | 6/6 | 2/6 | 2/6 | 2/6 | 4/4 |
| Qwen/Qwen3-4B | pt-BR | 6/6 | 3/6 | 2/6 | 2/6 | 2/4 |
| Qwen/Qwen3-4B | ta | 6/6 | 1/6 | 2/6 | 2/6 | 2/4 |
| Qwen/Qwen3-4B | zh-Hans | 6/6 | 2/6 | 2/6 | 2/6 | 3/4 |
| Qwen/Qwen3-4B | es | 6/6 | 2/6 | 2/6 | 2/6 | 4/4 |
| microsoft/Phi-4-mini-instruct | en | 1/6 | 4/6 | 4/6 | 3/6 | 0/4 |
| microsoft/Phi-4-mini-instruct | pt-BR | 6/6 | 1/6 | 4/6 | 4/6 | 0/4 |
| microsoft/Phi-4-mini-instruct | ta | 6/6 | 1/6 | 4/6 | 4/6 | 0/4 |
| microsoft/Phi-4-mini-instruct | zh-Hans | 5/6 | 0/6 | 4/6 | 4/6 | 0/4 |
| microsoft/Phi-4-mini-instruct | es | 5/6 | 1/6 | 4/6 | 4/6 | 0/4 |

Extraction checks five requirement fields. Fit correctness requires both the right decision and the complete unsupported-field list. Invalid outputs count as failures; they are not safe decisions.

The oracle supplies English-keyed correct requirements rather than the buyer conversation. Its language labels identify matched cases, not language present in the oracle prompt. Generated-record assessment consumes the exact retained extraction, including malformed text.

All sampled profiles, within-language repeat disagreements and matched English contrasts are retained in the JSON. Do not pool them as independent scenarios. No significance test, model competence gate, held-out evaluation or causal language ranking is supported. A zero field score after failed parsing does not prove semantic loss.

Independent language/domain review, native-authored paraphrases, more situation families and untouched evaluation cases are outstanding. These results assess internal discovery and fit only; they do not validate complete enterprise-sales agents.

[Frozen protocol](../experiments/sales-pilot/PROTOCOL.md).
