# Phi replication of the domain feasibility grid

Frozen October 27, 2026 before Phi collection. Repeat all 180 cases and four greedy stages from PROTOCOL.md: **720 planned Phi-4-mini-instruct calls**. No new cases, prompt changes, normalization repairs or altered scores. This is a second-model exploratory replication, not held-out confirmation or a validated industry benchmark.

Use the existing pinned Microsoft Phi revision and weight hashes. The same free T4, float16/no quantization, batch eight, Transformers 4.57.6, token caps, stage schedule and source/data preservation apply. Native model chat templates differ and must be recorded. Calls are collected in full, including failures; there is no automatic evaluation expansion.

Apply the same per-domain English screen (at least 5/6 full-history and 5/6 reference-record actions). Failed domains retain all results but do not support language attribution. Compare stage/format failures separately, and report model-specific gains and regressions rather than selecting the better model per case. Two small models do not establish production reliability, language rankings or cultural effects. All translations and domain rules remain unreviewed drafts.

Archive and verify the Qwen run before starting the Phi process. Never run duplicate collectors concurrently or use paid resources. Preserve any failed startup and all raw outputs. Model licenses remain separate from the software license.

```sh
python -m localesafe.collect_domain_replication --model phi4-mini --split development --output-dir reports/domain-study-phi4-mini
```
