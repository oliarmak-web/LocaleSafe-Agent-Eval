# Execution history

- CPU engineering prefixes: 124 decisions on Qwen3-0.6B and 48 on Qwen3-1.7B. Interrupted for a free T4 runtime transition. Every completed batch, original source and protocol is archived separately.
- First GPU pass: the notebook displayed completion markers for both grids, but temporary runtime files expired before retrieval. No numerical results from that pass are available or included in findings.
- Replacement GPU pass: same cases, prompts, decoding distribution and scoring. Sampled indices stay on the GPU to avoid unnecessary CPU synchronization. The archive is embedded in saved notebook output and downloaded, in addition to temporary runtime storage.

Only complete, retrieved and audited grids support the main results. CPU prefixes are not pooled with GPU results. The earlier unretrieved pass is not presented as an independent replication.
