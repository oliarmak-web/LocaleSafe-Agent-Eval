# Language or workflow? Controlled development study

Frozen before task collection. AI-authored draft translations; no independent human review. No preregistration or held-out benchmark claim.

## Questions and design

30 authored scenarios (six families × five variants), parallel English, Spanish, Simplified Chinese, Ukrainian and Haitian Creole. Two sampled repeats; repeats and template variants are clustered, not independent real-world situations.

Families: availability without booking, appointment correction, afternoon/excluded-day constraint, unavailable-slot alternative, interpreter language independent of US locale, English-to-target-language correction. Slot/day IDs remain invariant; this isolates linguistic instructions from date arithmetic and translated entity names.

- Baseline: English policy, target-language request. 300 decisions/model.
- Localized policy: same request and tool schema, translated policy. 240 decisions/model; English reuses its baseline.
- Structured facts: language-free canonical user facts replace the request. 60 decisions/model, shared across language pairs. This is an oracle interpretation intervention, not model-extracted facts.
- Recovery: inject a reachable wrong proposal, then a target-language rejection and correction. 300 decisions/model. This is a controlled two-turn history, not recovery from each model's own baseline errors.
- English restatement: reuse the matched English baseline for each non-English task. No translator was run. Parallel authored requests are not independently verified translations, so this is not a human-verified translation-rescue experiment.
- Replication: Qwen3-0.6B and Qwen3-1.7B, pinned public weights. Same family; the larger model is not assumed superior before results.

900 real generations/model; no paid API. CPU, four threads, float32 activations with dynamic int8 Linear weights for both models. This differs from earlier float32 probes. Batch size four; each row has its own seeded sampler. Matched initial conditions/languages share seeds; recovery uses separate matched seeds. Temperature 0.7, top-p 0.8, top-k 20, max 64 tokens, thinking disabled. No task-output tuning, retries, answer options, or output repair. An unrelated feasibility prompt tested the runtime before collection; it is not research data.

## Scoring

Model emits one JSON tool call. Primary parser accepts only exact JSON and valid tool schemas. Secondary parser strips only one enclosing Markdown JSON fence. Duplicate keys, extra prose, unsupported arguments and truncated outputs fail. Sandbox executes actual recorded calls against supplied state. Record parsing, exact tool/arguments, executable action, state completion and unauthorized mutation attempts separately. Canonical calls must pass all cases; injected wrong calls must fail task success.

All user requests withhold approval. Commit/cancel attempts are blocked and counted. There are no positive approval examples, real external services or full autonomous multi-step sessions. Passing denial tests cannot establish general consent competence. Recovery ends at the corrected proposal; no automatic approval or real booking follows.

## Analysis fixed before collection

Report every language and condition, strict and fence-only scores, per-family errors, and matched pairs: both correct, both wrong, English-only, other-only. Compare policy-language and structured-fact controls within scenario/repeat. Summarize both models separately. Reused English/oracle controls are not additional inference or independent observations.

No significance, language ranking, causal language disadvantage, cultural competence or operational-harm claim. A language-associated difference requires reviewed equivalence and replication. English restatement success suggests presentation sensitivity; oracle success suggests an interpretation bottleneck; oracle failure suggests remaining planning/interface issues. These are diagnostic hypotheses, not uniquely identified mechanisms.

Archive cases, full prompts, raw outputs, seeds, hashes, revisions, environment, collector and builder snapshots, scoring and all failures. Preserve interrupted prefixes on resume. Publish unsuccessful and null results alongside successes.

## Runtime amendment, before GPU collection

CPU collection proved slow. The primary complete runs move to a free Colab Tesla T4, float16 weights/activations, no quantization, batch size eight and two CPU threads. Both models use the same GPU collector, tasks, prompts, decoding distribution and per-row CUDA seeds. Python/package/CUDA versions are recorded in each manifest. CPU and GPU random streams and numerical precision differ: do not pool their outputs or interpret their difference as a language effect.

The partial CPU runs are retained as interrupted engineering runs, with original source and protocol. No task, prompt, scoring rule or output cap changes for the GPU run. The runtime amendment is not a response to a favorable language result; full GPU grids will include every scheduled decision and failure. No human review or paid compute is introduced.

## Recovery after temporary-runtime expiry

The first GPU notebook displayed BOTH_GPU_GRIDS_COMPLETE and RESULT_ARCHIVE_READY, but its temporary files expired before retrieval. No numerical results from that pass were inspected, retained or pooled. The archived study is a replacement full run of the same frozen tasks and settings. Its collector keeps sampled token indices on the GPU instead of copying each index to the CPU; sampling distributions, row seeds and scoring are unchanged. Original code remains in Git history. The replacement launcher embeds the compressed archive in saved notebook output and requests a download, in addition to keeping runtime files.
