# LocaleSafe

**Find out why a multilingual AI agent took the wrong action.**

LocaleSafe is a research toolkit for testing service agents across languages. It checks the action an agent chooses, the details it sends to a tool, and whether the user allowed the change.

Use it to investigate a practical question: **is the failure in language understanding, the workflow, the handoff, or the safety monitor?**

Created and maintained by **Olivia Iarmak**. MIT-licensed research prototype. Implementation, translations and documentation use AI assistance.

## The problem

An agent can answer fluently and still change the wrong appointment. A user can approve one action, then withdraw that approval in another language. A handoff can lose the correction, and a safety monitor can miss the mistake.

LocaleSafe helps you test these failures separately before choosing a fix. Example uses include appointment changes, customer-service requests and interpreter handoffs. Language, region and user preference are separate inputs.

## What this project contributes

- **Matched workflow experiments:** equivalent requests with fixed task details, plus controls for instruction language, structured facts and conversation history.
- **Action and outcome scoring:** format checks, exact tool arguments, sandbox state and permission checks.
- **An auditable experiment record:** prompts, raw outputs, failures, settings, source snapshots and artifact hashes.
- **A permission-handoff study:** separate scores for the handoff record, acting agent and monitor when the user changes permission across languages.

These are the project's concrete artifacts. Multilingual evaluation, authorization checks and monitor evaluation have established precedents. The current study tests how language, handoff contracts and monitor evidence affect permission-sensitive actions. [Method comparison](docs/HANDOFF_METHOD_COMPARISON.md). [Related work](docs/COMPETITIVE_LANDSCAPE.md) · [Authorship and provenance](CREDITS.md).

## Latest study: permission across language switches

**3,264 new model calls:** 576 summary generations, 1,152 actor decisions and 1,536 monitor judgments. The study uses 64 draft English/Spanish cases across eight templates, with separate development/evaluation families and greedy plus sampled decoding. Qwen3-4B passed the development English screen; SmolLM3-3B did not, so its evaluation run was skipped.

| Finding | Evidence | Implication |
|---|---|---|
| Language switching was not uniformly worse | Qwen answered all 32 development cases correctly from full history, across all four language patterns | Check workflow explanations before blaming language |
| A structured handoff can preserve permission and still fail | Qwen's greedy action score fell from 32/32 with full history to 23/32 with generated records | Check the action contract and downstream behavior, not only permission fields |
| More explicit monitor rules can create a tradeoff | False allows fell from 39/64 to 18/64; false blocks rose from 0/64 to 40/64 | Measure valid actions blocked as well as unsafe actions allowed |

Qwen preserved the permission, version and source fields in all 192 generated records across its two splits and three decoding profiles. Requested-action representation and monitor interpretation still failed. Perfect reference records produced 128/128 correct monitor judgments in the follow-up; they are an oracle control, not a working extraction solution.

The rule-prompt follow-up and cached routing replay are exploratory analyses designed after the initial results. Draft translations, eight templates and only one qualifying model limit generalization. These results do not establish causal language bias, a stable language ranking or production safety.

[Technical report and plain-English interpretation](docs/HANDOFF_TECHNICAL_REPORT.md) · [Complete result tables](docs/HANDOFF_RESULTS.md) · [Monitor intervention](docs/MONITOR_FOLLOWUP.md) · [Protocol](experiments/handoff-study/PROTOCOL.md).

## Earlier multilingual experiments

An earlier study recorded **1,800 decisions from two related Qwen3 models in five languages**: English, Spanish, Simplified Chinese, Ukrainian and Haitian Creole. Qwen3-1.7B returned 278/300 valid baseline commands, but only 37/300 were correct. Translating instructions gained six successes and lost eleven.

[Earlier findings](docs/FINDINGS.md) · [Workflow study](docs/WORKFLOW_STUDY.md) · [English rerun control](docs/CONSISTENCY_CONTROL.md).

## Try it locally

Python 3.11+. Scoring needs no packages, API keys, GPU or network. From a local checkout:

```sh
python -m localesafe.handoff_eval --cases experiments/handoff/cases.jsonl --traces experiments/handoff/stale_handoff.jsonl --trace-origin synthetic --output reports/handoff-stale.json
python -m unittest discover -s tests -v
```

The injected stale-handoff trace produces 48 unauthorized attempts. The sandbox blocks all 48. This verifies the bounded test executor, not a model's safety. The report includes component scores, final state and input hashes. Choose a new output filename for each run.

[Earlier experiments](experiments/README.md) · [Benchmark registry](docs/BENCHMARKS.md) · [Scoring](docs/SERVICE_SCORING.md).

## Use, contribute and cite

Useful contributions include independent bilingual review, new situation families, model adapters and independent reproductions. See [CONTRIBUTING.md](CONTRIBUTING.md). Do not add credentials or real customer conversations; see [SECURITY.md](SECURITY.md).

If you use the code, fixtures or analyses, cite **Olivia Iarmak, LocaleSafe**, identify the experiment and include the exact commit you used. Machine-readable citation: [CITATION.cff](CITATION.cff); BibTeX: [CITATION.bib](CITATION.bib). Cite the underlying Qwen and SmolLM models and any external datasets separately. The technical report is repository documentation; no journal publication, DOI or peer-reviewed validation is claimed.

For a concise explanation of the work and its evidence, see the [research brief](docs/RESEARCH_BRIEF.md). For provenance, see [credits](CREDITS.md) and [history](docs/HISTORY.md).

**Status:** exploratory research prototype. Independent bilingual review, broader model testing and external reproduction remain outstanding.
