# LocaleSafe

**Find where multilingual service agents fail: language, context, or workflow.**

LocaleSafe pairs equivalent requests, varies locale explicitly, and replays actions in a consent-aware sandbox. Its contribution is a runnable diagnostic harness for service workflows—not a claim to be the first multilingual benchmark.

## What works

| Component | Status |
|---|---|
| Language, locale, and phrasing comparisons | Implemented |
| Appointment-change and interpreter-handoff sandbox | Implemented; no real service calls |
| Format, intent, context, clarification, consent, tools, completion scorecards | Implemented |
| Sandbox controls | 11 draft English/Spanish episodes; synthetic traces |
| Real-model pilot | 108 Qwen3-0.6B outputs; nine language configurations; single-turn |
| Reviewed cultural-context benchmark | Not yet validated |

## Run

Python 3.11+. No packages, keys, GPU, or network needed to score traces.

```sh
python -m localesafe.service_eval --cases examples/service/cases.jsonl --traces examples/service/faulty-traces.jsonl --comparisons examples/service/comparisons.jsonl --trace-origin synthetic --output reports/service.json
python -m unittest discover -s tests -v
```

The faulty fixture passes 7/11 episodes. Four injected failures exercise consent, date context, clarification, and handoff. These are harness checks, not model results. Output paths must be new.

## Why this matters

A translated request can still trigger the wrong action. An English workflow defect can also look like a language problem. Score each stage before choosing a fix.

U.S. service use cases: municipal appointments, airport assistance, and interpreter handoff. Language does not determine nationality, date convention, or user preference. [U.S. rationale and research direction](docs/AUTHORED_RESEARCH_AGENDA.md).

## Evidence

The [local-model pilot](experiments/results/qwen3-06b-20261021/RESULTS.md) had 92/108 Markdown-wrapped answers that failed strict JSON parsing. A post-hoc fence-only diagnostic yielded 34/54 baseline passes and 31/54 checking-prompt passes. This is evidence of integration weaknesses—not established language bias.

[Scoring and schema](docs/SERVICE_SCORING.md) · [Benchmark registry](docs/BENCHMARKS.md) · [Experiments](experiments/README.md) · [Research protocol](docs/RESEARCH_PROTOCOL.md) · [Contribute](CONTRIBUTING.md) · [Security](SECURITY.md) · [History](docs/HISTORY.md)

Created by Olivia Iarmak; implementation and writing used AI assistance. MIT-licensed code. Draft translations and small samples do not establish causal language effects, cultural competence, clinical safety, or real-world impact.
