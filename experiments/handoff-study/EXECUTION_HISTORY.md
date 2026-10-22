# Handoff study execution history

Protocol and collector frozen in commit `3294437` before collection. Collection date: October 22, 2026. Source snapshots and protocol hashes are included in each archive.

## Initial collection

Free Colab Tesla T4; CUDA float16, no quantization; pinned Qwen3-4B and SmolLM3-3B weights. Actual Python, PyTorch, Transformers, CUDA and sampling settings are recorded in the manifests.

| Archive | Requests | Outcome |
|---|---:|---|
| `handoff-qwen3-4b-development-20261022` | 960 | Completed; English gate 8/8 in full-history and oracle-record conditions |
| `handoff-qwen3-4b-evaluation-20261022` | 960 | Completed after passing development gate |
| `handoff-smollm3-3b-development-20261022` | 960 | Completed; English gate 6/8 full history and 4/8 oracle record; evaluation not run |

Every scheduled request is preserved, including invalid outputs. The same model performs the summary, actor and monitor roles within its run. No paid inference API was used.

The Colab runtime later disconnected. Before further work, the complete ZIP embedded in the notebook output was saved locally and verified against its displayed SHA256:

```text
73692a445303002bd72d166acc830c30df1d5a696a98ece3413fc1f9f9697b0e
423221 bytes
```

The ZIP contained all three run directories. They were copied into `experiments/results/` with the date suffix; contents and raw bytes were preserved. Every internal archive hash, case split, prompt, dependency, seed and score is checked by the offline auditor. Chat-template render hashes remain recorded; validating those against a freshly rendered template additionally requires the pinned tokenizer.

## Exploratory follow-ups

The explicit-rule monitor intervention was designed after inspecting the initial results and frozen in commit `99368bf`. Its protocol and source snapshots identify it as exploratory. It repeats the original greedy monitor prompt, adds explicit permission checks, and supplies oracle records as a separate control. Original outputs remain unchanged.

All 384 follow-up requests completed on a free T4 with the same runtime versions and pinned Qwen weights. The locally preserved ZIP was 126976 bytes, SHA256 `c1b4217d586cc641e07a82f32ef99e6e9d179992042d57fbbd960323c6f47887`. Every baseline-repeat verdict matched the original greedy monitor judgment. The archived run is `monitor-followup-qwen3-4b-20261022`.

The schema-validation routing replay was also designed post-hoc. It selects between existing generated-record and full-history actor outputs. It makes no new model calls and is not a newly deployed routing experiment. A valid record schema does not authenticate the permission it claims.

Independent bilingual review has not been performed. Instructions for a blinded review are in [REVIEW.md](REVIEW.md). Dataset corrections require explicit versioning and cannot silently replace the archived inputs.

## Mistral and Phi extension

Both additional development runs completed 960 calls. Both failed the pre-existing English gate and neither evaluation split was run. The combined ZIP preserved from Colab contains both runs: 319492 bytes, SHA256 `84b01a199d46f83405e3a8fc998329fcc49adc403aa0af4039c9c8ef7ac40424`. It was checked before extraction; each internal archive, schedule, prompt, score and input split passed the offline auditor.

The initial Mistral startup was interrupted during download before inference was reported. The revised startup used a new directory and loaded weights directly to GPU. Frozen tasks and scoring were unchanged. Mistral used batch size 1, Phi batch size 8. Extension source snapshots and model pins are retained inside both archives.
