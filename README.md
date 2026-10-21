# LocaleSafe

**A research scaffold for evaluating multilingual agent escalation, clarification, and tool-call behavior.**

Originated in Olivia Iarmak's December 2025 hackathon simulation. This October 2026 implementation evolves that concept into a deterministic offline evaluator. It is an early research tool, not a validated safety benchmark. No real-model experiment has been conducted in this release.

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

This version scores **recorded, single-turn text behavior**, not audio, reasoning quality, hallucination, or clinical correctness. The mock assistance tool is only a label in JSON; it cannot dispatch anything. Scenario expectations are illustrative research policies, not operational emergency guidance. Current public test cases are examples, not a contamination-resistant held-out benchmark. No confidence intervals or significance claims are supported by the tiny fixtures.

See [history](docs/HISTORY.md), [research protocol and v2](docs/RESEARCH_PROTOCOL.md), [dataset notes](examples/README.md), [security](SECURITY.md), and [contributing](CONTRIBUTING.md).
