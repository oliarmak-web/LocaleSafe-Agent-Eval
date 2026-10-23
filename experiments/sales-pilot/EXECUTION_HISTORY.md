# Sales pilot execution history

October 23, 2026, America/New_York. The pilot's collector, dataset, scoring and protocol were frozen in commit `f54bc84` before collection. The independent offline auditor was added afterward without changing the collector or cases.

The uploaded package SHA256 is `e733d8e457568eaf12dcb8202e029d9f8c3aab453e567766214c609ecb95b079`. The free Colab T4 session connected successfully. A new cell starts Qwen3-4B and then Phi-4-mini with 360 scheduled calls each. Existing notebook outputs are preserved. Collection begins with requirement extraction before dependent generated-record assessments.

Initial status: collection started; results had not yet been audited or reported. Count only verified retained calls after completion. No independent language or domain review has occurred. Draft pilot outputs cannot establish a validated language gap or real commercial impact.


## Completed collection

Both models completed 360 calls, 720 retained calls total, on the free GPU. Qwen's first ZIP was 123011 bytes, SHA256 `0e950ba06a3b299634535917ef55a42df53706d5af08d0fc718c508de8f938c3`. The final combined ZIP was 174728 bytes, SHA256 `a201d83906ff51ec2d0daadf52a31916d6853fddd66147e5b03bc2ffb788a9d0`. Both displayed hashes were checked before extraction. The Qwen files in the final ZIP exactly match the first preserved archive.

Run folders were copied without changing raw bytes to `experiments/results/sales-qwen3-4b-20261023` and `sales-phi4-mini-20261023`. Archive inventories, hashes, frozen cases/design, source snapshots, complete schedules, prompt dependencies, seeds, token limits and recomputed scores passed the offline auditor. The original Windows input JSONL used CRLF; the collector's selected-case serialization on Linux used LF. The auditor verifies both complete byte forms plus exact parsed frozen cases; it does not rewrite archived data or ignore arbitrary differences. A regression test exercises this distinction.

All draft review labels remain unchanged. No real commercial actions, sent proposals or human reviews occurred. Derived tables and matched comparisons are separate from immutable runs. Collector prompts and scoring were not changed after collection began.
