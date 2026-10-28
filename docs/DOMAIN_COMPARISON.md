# Domain comparison: language, policy and representation

1,440 recorded calls: two small models, five fictional policies, six languages and six shared intent families. This is exploratory text research, not a validated industry benchmark or cultural study.

## Full-history exact actions

| Model | Domain | en | es | hi | pt-BR | zh-Hans | ta | English screen |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Qwen3-4B | security | 5/6 | 5/6 | 2/6 | 5/6 | 4/6 | 2/6 | passed |
| Qwen3-4B | finance | 5/6 | 5/6 | 2/6 | 5/6 | 4/6 | 2/6 | passed |
| Qwen3-4B | health_admin | 5/6 | 5/6 | 2/6 | 4/6 | 4/6 | 2/6 | passed |
| Qwen3-4B | insurance | 4/6 | 4/6 | 2/6 | 4/6 | 3/6 | 1/6 | failed |
| Qwen3-4B | telecom | 5/6 | 4/6 | 2/6 | 4/6 | 4/6 | 3/6 | passed |
| Phi-4-mini | security | 5/6 | 5/6 | 4/6 | 5/6 | 4/6 | 3/6 | failed |
| Phi-4-mini | finance | 3/6 | 3/6 | 4/6 | 3/6 | 3/6 | 5/6 | failed |
| Phi-4-mini | health_admin | 3/6 | 3/6 | 3/6 | 3/6 | 2/6 | 4/6 | failed |
| Phi-4-mini | insurance | 4/6 | 4/6 | 4/6 | 4/6 | 3/6 | 3/6 | failed |
| Phi-4-mini | telecom | 4/6 | 3/6 | 1/6 | 4/6 | 2/6 | 2/6 | failed |

A screen requires at least 5/6 English full-history and 5/6 reference-record actions. Phi failed every domain; Qwen failed insurance. Do not interpret failed domains as language-attribution evidence. Passing a six-case screen does not establish broad domain competence.

## Evidence conditions and rejected attempts

| Model | Evidence | Exact correct | Contract valid | Rejected executes | Guard blocks |
|---|---|---:|---:|---:|---:|
| Qwen3-4B | qualify_history | 108/180 | 166/180 | 19 | 19 |
| Qwen3-4B | qualify_oracle | 156/180 | 180/180 | 18 | 18 |
| Qwen3-4B | qualify_generated | 127/180 | 180/180 | 15 | 15 |
| Phi-4-mini | qualify_history | 103/180 | 172/180 | 1 | 1 |
| Phi-4-mini | qualify_oracle | 120/180 | 174/180 | 24 | 24 |
| Phi-4-mini | qualify_generated | 82/180 | 138/180 | 13 | 13 |

These are repeated checkpoint responses, not independent callers or production failure rates. Guard blocks are separate code enforcement. Reference records can improve aggregate correctness while still producing forbidden attempts; they are not a demonstrated mitigation.

## Reference and measurement concerns discovered during analysis

- Conditional messages explicitly say wait, while the authored extraction schema stores the ultimate execute intent with conditional approval. This is an author convention requiring independent review, not established misunderstanding when a model extracts wait.
- Insurance values require an object; a JSON-encoded string preserving both dates still fails exact field fidelity. Zero exact records is not zero comprehension.
- Acknowledgment retains a pending proposal under the authored checkpoint rule; these histories do not simulate an already completed live interaction.

The original labels and all outputs remain intact. Future adjudication needs independent review and a new versioned case set. No score repair or favorable-case selection was applied.

[Qwen detail](DOMAIN_QWEN_RESULTS.md) · [Phi detail](DOMAIN_PHI_RESULTS.md) · [Cases, local export and scoring](DOMAIN_AND_SPEECH_STUDY.md).
