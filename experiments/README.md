# Real-model pilot

**Completed:** Qwen3-0.6B, 108 local CPU generations, two prompts, nine language configurations. No paid inference or tool execution.

[Results](results/qwen3-06b-20261021/RESULTS.md) · [Diagnostics](results/qwen3-06b-20261021/LANGUAGE_DIAGNOSTICS.md) · [Benchmark registry](../docs/BENCHMARKS.md)

## Reproduce

Use a virtual environment. Downloads require internet and disk; CPU inference uses local resources.

```sh
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install "transformers>=4.51,<5"
python experiments/download_pilot_model.py
python -m localesafe.collect_local --cases experiments/pilot-cases.jsonl --output-dir reports/local-pilot --model Qwen/Qwen3-0.6B --revision c1899de289a04d12100db370d81485cdf75e47ca --local-model-dir private/qwen3-06b
```

The downloader verifies about 1.5 GB of weights. The [model license](https://huggingface.co/Qwen/Qwen3-0.6B) is separate from our code license. Exact runtime versions are archived with results. Output directories must be new.

## Design

Six families × English, Spanish, Simplified Chinese text, Vietnamese, Tagalog, Arabic, Korean, Ukrainian, Haitian Creole. All translations are draft. This is neither a representative U.S. sample nor a cultural-competence benchmark.

Baseline: fixed policy + JSON contract. Check: same policy + information-checking instruction. Jobs are interleaved with fixed seeds; one generation per item/condition. All raw prompts, outputs, failures, timings, hashes, and settings are retained. No gold labels enter prompts; no hidden retries or output repair.

Strict passes: 8/54 and 1/54. Post-hoc fence-only passes: 34/54 and 31/54. These are two conditions on one model, not independent studies. The intervention did not improve this run.

## Audit

```sh
python -m experiments.summarize_pilot experiments/results/qwen3-06b-20261021
```

Analysis verifies hashes and recomputes scores. Fence-only and language-attribution diagnostics were added after initial output inspection. Archived bytes are preserved across platforms. An earlier loader download stalled before inference; it is excluded from completed results.

The v0.2 service sandbox has synthetic controls only. New model/dialogue collection, independent reviews, held-out families, and repeated runs are next.
