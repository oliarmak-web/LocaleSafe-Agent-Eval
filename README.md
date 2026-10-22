# LocaleSafe

**Find where multilingual service agents fail: language, context, or workflow.**

**Research question:** when an agent works in English, does it still work on the same request in another language—and what extra tests or monitoring would reveal failures?

LocaleSafe pairs equivalent requests, varies locale explicitly, and replays actions in a consent-aware sandbox. Its contribution is a runnable diagnostic harness for service workflows—not a claim to be the first multilingual benchmark.

**Latest study:** 1,800 tool decisions, two models, five languages, four conditions. [Methods and results](docs/WORKFLOW_STUDY.md).

- **A command can look right and still do the wrong thing:** the larger model returned 278/300 correctly formatted commands, but only 37/300 chose the right action and details.
- **Language differences changed with the model:** the small model corrected 58/60 English proposals and 2/60 Haitian Creole proposals. The larger model scored 10/60 and 16/60. There was no consistent ordering.
- **Translation alone was not a dependable fix:** translating the larger model's instructions gained six successes and lost eleven. Giving it the correct facts directly also failed to reliably solve the task.

These are development findings from draft translations and six template families. They motivate evaluation; they do not establish causal language bias or deployment safety.

[Findings in plain English](docs/FINDINGS.md) · [Why this is credible and useful](docs/WHY_IT_MATTERS.md)

[What multilingual evaluation and monitoring should add](docs/MULTILINGUAL_EVAL_MONITORING.md). Evaluation is implemented; live production monitoring is a proposed next step.

[Plan for a stronger, reviewed study](docs/V1_RESEARCH_PLAN.md): permission and correction failures, normal model variation, and monitoring effectiveness. The current release is exploratory.

## What works

| Component | Status |
|---|---|
| Language, locale, and phrasing comparisons | Implemented |
| Appointment-change and interpreter-handoff sandbox | Implemented; no real service calls |
| Format, intent, context, clarification, consent, tools, completion scorecards | Implemented |
| Sandbox controls | 11 draft English/Spanish episodes; synthetic traces |
| Real-model pilot | 108 Qwen3-0.6B outputs; nine language configurations; single-turn |
| Controlled attribution probe | 30 tasks; 180 model forwards; 540 sampled choices; closed-choice |
| Direct-answer cross-check | 80 generations; English, Spanish, Chinese, Ukrainian, Haitian Creole; numeric and explicit dates |
| Matched workflow study | 1,800 generations; two models; policy, structured-fact and seeded correction controls |
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
