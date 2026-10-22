# Execution history

- CPU engineering prefixes: 124 decisions on Qwen3-0.6B and 48 on Qwen3-1.7B. Interrupted for a free T4 runtime transition. Every completed batch, original source and protocol is archived separately.
- First GPU pass: the notebook displayed completion markers for both grids, but temporary runtime files expired before retrieval. No numerical results from that pass are available or included in findings.
- Replacement GPU pass: same cases, prompts, decoding distribution and scoring. Sampled indices stay on the GPU to avoid unnecessary CPU synchronization. The launcher embeds the archive and requests a download. A separately saved notebook copy retains the embedded archive despite an automatic-save conflict in the original research notebook.
- Retrieval: browser download capture failed. A compact export retained raw outputs, token counts, batch timings and original manifests. Repeated fields were reconstructed from frozen code and pinned tokenizers; both restored raw JSONL files match the original Colab SHA-256 values exactly. All 900 decisions per model passed the local audit. No numerical result from the earlier lost pass is included.

Only complete, retrieved and audited grids support the main results. CPU prefixes are not pooled with GPU results. The earlier unretrieved pass is not presented as an independent replication.
