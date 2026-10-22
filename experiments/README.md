# Real-model pilot

Latest: [permission-handoff study](../docs/HANDOFF_TECHNICAL_REPORT.md), with 2,880 initial model calls, 384 exploratory monitor calls and a cached routing replay. [Protocol](handoff-study/PROTOCOL.md) · [Execution history](handoff-study/EXECUTION_HISTORY.md). The earlier [48-case prototype](handoff/PROTOCOL.md) remains a separate synthetic control set.

## Latest: matched workflow study

[Study and findings](../docs/WORKFLOW_STUDY.md) · [Protocol](workflow/PROTOCOL.md) · [Execution history](workflow/EXECUTION_HISTORY.md)

**1,800 recorded tool decisions:** Qwen3-0.6B and Qwen3-1.7B on a free Colab T4. Five languages; six template families; two repeats. Baseline, localized policy, canonical structured facts, and seeded rejected-proposal correction.

The larger model produced 278/300 valid baseline calls but only 37/300 correct actions. Canonical facts and localized policies did not reliably fix it. Correction scores changed sharply by model and language; no stable language ranking was established.

| Archive | Decisions | Evidence |
|---|---:|---|
| [Qwen3-0.6B](results/workflow-gpu-qwen3-06b-20261022/RESULTS.md) | 900 | Full prompts, raw outputs, scores, source and hashes |
| [Qwen3-1.7B](results/workflow-gpu-qwen3-17b-20261022/RESULTS.md) | 900 | Same grid and runtime |
| Interrupted CPU runs | 124 + 48 | Preserved separately; excluded from the comparison |

```sh
python -m experiments.summarize_workflow experiments/results/workflow-gpu-qwen3-06b-20261022
python -m experiments.summarize_workflow experiments/results/workflow-gpu-qwen3-17b-20261022
python -m experiments.compare_workflow experiments/results/workflow-gpu-qwen3-06b-20261022 experiments/results/workflow-gpu-qwen3-17b-20261022
```

For new collection on a CUDA GPU: install Transformers 4.57.6 and a compatible PyTorch build, then run `python -m localesafe.workflow_gpu --model qwen3-06b --output-dir reports/new-workflow`. Repeat with `qwen3-17b`. The collector downloads pinned public weights and verifies their hashes; no credentials or paid API are required. Complete runtime versions are recorded for the relevant Python, PyTorch, Transformers and CUDA components in each manifest.

The first GPU pass completed but its temporary archive was lost before retrieval. The published replacement preserves every scheduled output; restored raw-file hashes match the originals from Colab. [Transfer provenance](results/workflow-gpu-qwen3-06b-20261022/TRANSFER.md).

## Earlier: direct answers in five languages

[Results](results/direct-five-language-20261021/INSIGHTS.md) · [Protocol](direct/PROTOCOL.md)

80 local generations across English, Spanish, Simplified Chinese, Ukrainian, and Haitian Creole. No answer options. Numeric dates vary explicit locale; ISO and localized dates are controls.

24/80 interpretations were correct. There were 36 unnecessary clarification requests and 19 invalid scalar outputs. A scripted-reply defect caused 12 of 13 original wrong sandbox commits. Post-hoc replay with corrected replies yields 1 wrong commit and 60/80 completions; model answers remain unchanged. This is a workflow-fixture repair, not improved model understanding.

```sh
python -m experiments.summarize_direct experiments/results/direct-five-language-20261021
python -m localesafe.direct_probe --cases experiments/direct/cases.jsonl --model-dir private/qwen3-06b --output-dir reports/direct-new
```

Current development fixtures correct the scripted reply. Archived fixtures preserve the original defect; use archived cases and source snapshots to reproduce the original run. The repair analysis was added after collection. All translations remain draft; one small model cannot establish a language effect.

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

## Controlled attribution probe

[Protocol](attribution/PROTOCOL.md) · [Results](results/attribution-20261021/INSIGHTS.md) · [Plain-language findings](../docs/FINDINGS.md)

30 tasks, six balanced answer orders, three seeded draws per order. Closed-choice probabilities remove JSON formatting but revealed strong label-position sensitivity. Repeated draws reuse probabilities; they are not independent tasks or free-form generations.

```sh
python -m experiments.summarize_attribution experiments/results/attribution-20261021
```

Collection can resume with `--resume` using the original arguments. Completed forward groups are validated and preserved; changed settings, duplicates, and partial groups are rejected. The archived run resumed after 128/180 forwards. No earlier choice was discarded or retried.

The earlier workflow study adds bounded tool decisions and seeded correction histories. The later handoff study introduces family-separated cases and a second model family, but only Qwen passes its development competence screen. Full autonomous dialogue and independent review remain outstanding.
