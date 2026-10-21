# Exploratory local pilot

This pilot compares two prompts on one real, small, open-weight model. No paid inference, provider API keys, or public UI is involved. Local hardware, electricity, storage, and model/runtime downloads are still required. Dependency downloads and the first model download require internet; inference occurs on the local CPU. No user scenarios are sent to a hosted model API.

The October 21, 2026 run completed all 108 generations. Read [results](results/qwen3-06b-20261021/RESULTS.md), [stage/paired diagnostics](results/qwen3-06b-20261021/LANGUAGE_DIAGNOSTICS.md), and the [benchmark registry](../docs/BENCHMARKS.md). No established external benchmark was run.

## Scope

54 draft cases = six scenario families × nine language configurations: English, Spanish, Simplified Chinese text, Vietnamese, Tagalog, Arabic, Korean, Ukrainian, Haitian Creole. These are deliberately a mixture of U.S. service-relevance and author/project relevance, not a ranking of languages or a representative sample of U.S. residents. Written Chinese does not represent all Chinese language varieties; standard written Arabic does not evaluate spoken dialects. Text does not measure accents, speech, ASR, or accessibility generally.

Language choice should eventually use target-community data, limited-English-proficiency needs, failure exposure, and access to qualified reviewers. The [Census language tables](https://www.census.gov/newsroom/press-releases/2025/2017-2021-acs-language-use-tables.html) provide a demographic starting point, not a safety ranking. Spanish is prioritized; other included languages provide distinct scripts and translation review needs. Haitian Creole is an exploratory service-access extension. Ukrainian retains continuity with the original project. No independent translation or domain-policy review has occurred.

The [NYC language-access hub](https://www.nyc.gov/site/immigrants/language-needs/language-access-hub.page) includes Haitian Creole, Korean, Arabic, Chinese, and Spanish among its designated translated languages, supporting a practical local service-access rationale for those selections. The pilot does not cover all NYC-designated languages and does not establish compliance with any language-access requirement.

## Two exploratory conditions

1. `baseline`: a fixed illustrative airport-assistance policy and JSON decision contract.
2. `check`: the identical policy plus a final urgency, negation, and required-information check.

This is a **prompt comparison**, not two independent studies or a native function-calling benchmark. The model generates decisions and proposed calls in JSON; no external action is executed. All messages, raw outputs, failures, input hashes, pinned model revision, decoding parameters, seeds, latency, and package versions are retained. No reasoning trace is requested or scored. Conditions/cases are interleaved in a fixed seeded random order. Sampling seeds match for each case across conditions, but different prompt lengths mean randomness is not perfectly coupled.

The policy instructs clarification for underspecified requests; emergency scenarios currently include a gate. This is not a clinically reviewed emergency policy. One generation per item and only six underlying families cannot support population-level safety, fairness, or intervention-efficacy claims. Both public dev and public test examples are included for exploration; neither is a held-out confirmatory evaluation. All output failures count against the primary pass rate. Escalation error counts cover parseable decisions; invalid generations are listed separately.

## Reproduce

Use a separate virtual environment. Install CPU PyTorch from its official index and Transformers from PyPI; see the exact package versions retained with a completed run. Model weights have their own [Apache-2.0 model license](https://huggingface.co/Qwen/Qwen3-0.6B), not the repository code license.

```sh
python -m venv .venv
# Activate the environment using your operating system's normal command first.
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install "transformers>=4.51,<5"
```

```sh
python experiments/build_pilot_cases.py
python -m localesafe.collect_local --cases experiments/pilot-cases.jsonl --output-dir reports/local-pilot --model Qwen/Qwen3-0.6B --revision MODEL_COMMIT_SHA
```

Use an immutable model SHA recorded in the run manifest. New output directories are mandatory, avoiding accidental overwrite. No hidden retries or JSON repair are performed; malformed outputs are retained as failures. A failed process leaves a started manifest and partial attempt log for inspection; do not call it a completed run. Results must be reviewed before being committed; do not commit model weights, environments, or caches.

For the fixed Qwen3-0.6B pilot, `python experiments/download_pilot_model.py` provides a checksum-verified direct-download alternative if the normal loader stalls. It downloads about 1.5 GB of weights into ignored `private/qwen3-06b/` and gets the tokenizer/config from the pinned official repository. Then pass `--local-model-dir private/qwen3-06b --revision c1899de289a04d12100db370d81485cdf75e47ca` to the collector. It records the weights hash. The model/config and runtime must still be trusted; disabling remote code is not a complete supply-chain guarantee.

## Next steps

Broaden scenario families and add challenge cases (negation, indirect distress, code-switching, distractors, incorrect tool locations), independent review, more capable comparison models, repeated generations, uncertainty analysis, and native tool-calling/multiturn controlled tool simulators. A v2 claim requires new frozen evaluation cases, not optimizing and re-testing these pilot cases.

## Regenerate descriptive analysis

```sh
python -m experiments.summarize_pilot experiments/results/qwen3-06b-20261021
```

This verifies case/attempt hashes, recomputes primary scores from raw attempts, and writes results plus strict and post-hoc language/workflow diagnostics. Raw archived bytes are preserved by `.gitattributes` so hashes remain valid across operating systems. Analysis is not preregistered; the fence-only diagnostic and language-attribution tables were added after initial output inspection. The first normal-loader download stalled before inference; its incomplete local directory was excluded from completed artifacts. The successful run used the checksum-verified direct download. No predictions were retried or removed from that successful run.
