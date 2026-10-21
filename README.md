# LocaleSafe

**A research scaffold for evaluating multilingual agent escalation, clarification, and tool-call behavior.**

Originated in Olivia Iarmak's December 2025 hackathon simulation. This October 2026 implementation evolves that concept into a deterministic offline evaluator. It is an early research tool, not a validated safety benchmark. A genuine local-model pilot has now been completed: 108 generations from Qwen3-0.6B across two prompts and nine language configurations. See the [results](experiments/results/qwen3-06b-20261021/RESULTS.md) and [language-versus-workflow diagnostics](experiments/results/qwen3-06b-20261021/LANGUAGE_DIAGNOSTICS.md).

## Run locally

Python 3.11 or later; no dependencies, credentials, GPU, or network access required for evaluation. From the repository root:

```sh
python -m localesafe.cli --cases examples/cases.jsonl --responses examples/synthetic-failures.jsonl --output reports/demo.json --run-label synthetic-fixture-not-a-model
python -m unittest discover -s tests -v
```

The output path must be new: reports cannot silently overwrite earlier results. Optionally install with `python -m pip install -e .` to use the `localesafe` command.

The example has 18 cases: six scenario families in English, Spanish, and Ukrainian. Non-English text is **draft and not independently reviewed**. The deliberately faulty fixture fails three cases. This verifies the evaluator; it is not evidence of model performance or language bias.

## What it measures

- Exact decision correctness: `escalate`, `clarify`, or `respond`.
- Exact tool-call agreement, including arguments and duplicate calls; call order is ignored.
- Missed and unnecessary escalation counts.
- Paired English-minus-language pass-rate gaps, matching the same scenario families.

Passing requires both the expected decision and expected tool calls. A positive paired gap means English passed more often in those pairs; it does **not** establish discrimination or causal bias. Reports include denominators, case-level failures, draft-translation warnings, artifact SHA-256 hashes, runner version, Python version, and a user-supplied run label.

## Bring your own agent responses

Keep cases fixed, run your agent separately, and save one response for every case:

```json
{"id":"urgent-en","decision":"escalate","tool_calls":[{"name":"request_assistance","arguments":{"location":"B14","priority":"urgent"}}]}
```

`examples/cases.jsonl` defines the case contract. Unknown IDs, missing responses, duplicate IDs, invalid tool-call structures, and scenario families spanning development and test splits are rejected. Expected labels must never be included in the agent prompt. Record the model, prompt, decoding configuration, and raw outputs separately as described in [the protocol](docs/RESEARCH_PROTOCOL.md). No provider adapter is implemented yet.

## Scope and limits

This version collects and scores **single-turn text decisions from a real local model**, or scores your recorded responses. It does not evaluate audio, reasoning quality, hallucination, or clinical correctness. The proposed assistance tool is only a label in JSON; it cannot dispatch anything. Scenario expectations are illustrative research policies, not operational emergency guidance. Current public test cases are examples, not a contamination-resistant held-out benchmark. The pilot is descriptive and does not support statistical significance or causal language-effect claims.

See [history](docs/HISTORY.md), [research protocol and v2](docs/RESEARCH_PROTOCOL.md), [dataset notes](examples/README.md), [security](SECURITY.md), and [contributing](CONTRIBUTING.md).

**What benchmarks do we run?** Currently, our own draft scenario suite and engineering controls. BFCL, MASSIVE-Agents, and Ticket-Bench are references/candidates, **not completed benchmark runs**. The [benchmark registry and attribution design](docs/BENCHMARKS.md) distinguishes datasets, metrics, formatting failures, and language-associated disagreements.

The [authored research agenda](docs/AUTHORED_RESEARCH_AGENDA.md) proposes a detailed v2 benchmark for U.S. service workflows: municipal request completion, airport assistance, clarification, consent, and human handoff. It includes U.S. motivation, twelve challenge families, experimental controls, metrics, related-work overlap (including MLCL), and a transparent authorship path. It is a design draft, not a completed benchmark or manuscript submission.

## Local model experiments

An optional [local collector and exploratory pilot protocol](experiments/README.md) extends the offline scorer to genuine model-generated decisions. The draft pilot includes 54 cases in nine language configurations. Inference runs on your CPU, with no paid model API or key; installing the separate PyTorch/Transformers runtime and downloading model weights requires internet and disk space. Nothing is hosted publicly. The dependency-free scoring commands above still work without that runtime.

The collector pins a model revision, excludes gold labels from prompts, records exact prompts and raw outputs, interleaves conditions, and keeps malformed outputs in the primary pass-rate denominator. This is JSON decision generation, not native tool execution or a validated emergency service. See the pilot documentation for reproduction and limitations.

**First finding:** 92/108 outputs violated strict JSON formatting because they were wrapped in Markdown fences. Strict task passes were 8/54 for baseline and 1/54 for the check prompt. A separately labeled post-hoc fence-only parser yields 34/54 and 31/54. English and most languages passed 4/6 baseline cases after fence removal; Haitian Creole and Tagalog passed 3/6. This small draft pilot identifies integration weaknesses and candidate disagreements; it does not establish general language bias. The extra-check prompt did not improve this run.
