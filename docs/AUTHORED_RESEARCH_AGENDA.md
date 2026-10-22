# From translation to task completion

Research agenda · Olivia Iarmak, creator and maintainer · October 21, 2026

**Contribution:** an open service-agent harness that separates language/context interpretation from consent, execution, and completion failures.

**Central question:** does success in English carry over to the same task in another language, and what additional evaluation or monitoring catches failures? The current experiments address controlled evaluation. [Language-aware production monitoring](MULTILINGUAL_EVAL_MONITORING.md) remains a research proposal.

## Why the U.S. should care

The Census Bureau reported that 22% of residents age 5+ spoke another language at home in 2017–2021. That is not the share needing interpretation. It establishes a domestic design context, not demand for any particular AI system. [Census source](https://www.census.gov/newsroom/press-releases/2025/2017-2021-acs-language-use-tables.html).

NYC provides interpretation and translated service information. Where organizations introduce agents, tests should reflect the people they serve. Agents should support accountable staff and interpreters, including reliable handoff. [NYC language-access hub](https://www.nyc.gov/site/immigrants/language-needs/language-access-hub.page).

## Use cases

| Workflow | Consequential failure |
|---|---|
| Municipal appointment/request | Wrong date, invented address, duplicate or unauthorized submission |
| Airport assistance | Wrong gate, lost accessibility requirement, failed handoff |
| Disaster-resource navigation | Stale availability or unsupported accessibility claim |
| Healthcare administration | Wrong appointment or lost interpreter preference; no diagnosis |
| Workplace intake | Lost negation/location or unsupported routing |

Only appointment changes and interpreter handoff are implemented in the current service sandbox. These are fictional workflows, not agency integrations.

## Study design

Compare equivalent requests while independently varying language, phrasing, and explicit locale. Replay canonical actions to test the executor. Score interpretation, clarification, consent, handoff, and completion separately. A date convention is task context—not a stereotype inferred from language.

Next challenge families: missing information, indirect requests, negation, code switching, date ambiguity, corrections, duplicates, denied consent, interpreter requests, and tool outages. Add reviewed cases before claiming coverage.

## Authorship and evidence

Substantive contributions: problem formulation, scenario/policy design, review coordination, simulator development, experiments, analysis, and writing. Credit actual work and reviewers with permission. Implementation and writing used AI assistance.

Planned outputs: design note → reviewed benchmark report → held-out empirical study → practitioner guide. No publication, adoption, endorsement, or impact claim is implied. HQ Labs affiliation remains unconfirmed.

[MLCL](https://arxiv.org/abs/2601.05366) already separates semantic and execution errors. [MASSIVE-Agents](https://aclanthology.org/2025.findings-emnlp.1099/) already benchmarks multilingual function calling. Our proposed extension is explicit service-workflow controls and consent/handoff outcomes, not a claim of being first.

[Scoring](SERVICE_SCORING.md) · [Protocol](RESEARCH_PROTOCOL.md) · [Benchmark status](BENCHMARKS.md)
