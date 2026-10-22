# Additional model replication

Specified October 22, 2026, before collecting additional model outputs.

Run Mistral-7B-Instruct-v0.3 and Phi-4-mini-instruct on the existing frozen English/Spanish cases. Model revisions and weight hashes are pinned in the collector. Preserve all outputs, including failures. These extend model coverage; they do not introduce unseen task families or independent translation review.

Keep prompts, task labels, decoding profiles, token limits, scoring and the development gate unchanged. Require at least 7/8 greedy English development successes under both full history and the reference record before running the evaluation split. Do not tune prompts after a failed screen.

Use unquantized float16 on the free Colab GPU. Mistral uses batch size 1 to fit memory; Phi uses batch size 8. Batch size is recorded in the manifest; runtime differences limit direct numerical comparisons. The collector excludes Mistral's redundant consolidated weight file, retaining and verifying the Transformers shards. Record source snapshots for this extension; previous archives remain unchanged.

Run development first, then evaluation only if the gate passes. Archive each completed split. Report model loading, memory or runtime failures separately from task failures. A failed run is not a completed experiment.

Kimi and hosted frontier models are not included: this protocol has no paid API budget or configured hosted endpoint. Tamil, Chinese and Ukrainian expansion remains separate planned work.
