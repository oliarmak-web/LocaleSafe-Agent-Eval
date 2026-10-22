# Originality and authorship

**Review date: October 21, 2026.** LocaleSafe has close precedents. This review does not establish that the project, its methods or its name are unique.

## What the search found

| Project | Overlap | LocaleSafe's current focus |
|---|---|---|
| [LangDrift](https://github.com/RubenGlez/langdrift) | Same intent across languages; tool and argument checks; failure categories; synthetic and real-model runs | Service-workflow sandbox and paired policy, structured-fact and seeded-correction experiments |
| [IndicOrderBench](https://github.com/Lingikaushikreddy/indicorderbench) | Final backend state, corrections, cancellation and duplicate-action checks; multilingual fixtures and CI | Text appointment and interpreter workflows; five-language, two-model development study |
| [BankBench](https://github.com/Sinar/BankBench) | Multilingual agent safety and domain-specific policies | Permission and correction in service workflows, with language and workflow explanations tested separately |

These descriptions come from the projects' READMEs inspected through GitHub. This is a scope comparison, not a source-code similarity audit. Their existence rules out claiming that multilingual tool evaluation, final-state scoring or a runnable multilingual harness is new by itself.

Relevant research also includes [Actions Speak Louder than Words](https://arxiv.org/abs/2608.11110), which examines cross-language action-policy retention and within-language inconsistency, and [GAIA-v2-LILT](https://arxiv.org/abs/2604.24929), which addresses multilingual benchmark adaptation. English self-consistency controls and translation validation are established methodological needs, not inventions of this project.

## Search scope and limits

Authenticated GitHub searches included:

```text
LocaleSafe
langdrift
multilingual agent benchmark in:name,description
multilingual safety evaluation in:description
```

The name search returned only this repository. Two targeted code searches returned no matches:

```text
"def compile_date(case, selected)"
"wrong_executed_action" "baseline_vs_structured_facts"
```

These are limited searches. Private, unindexed, differently named and independently developed work can be missed. Two unmatched snippets do not prove that every file is original. No comprehensive clone detection, license audit or trademark review was performed. The results do not establish priority: repository dates alone would not prove who first developed an idea.

Archived source snapshots inside LocaleSafe intentionally repeat code to preserve experiment provenance. They are not separate contributions and should remain intact.

## Authorship statement

Olivia Iarmak is LocaleSafe's creator and maintainer. She supplied the project direction, use cases, research questions and priorities. Code, scenario drafts, translations, analysis tooling and documentation were developed with AI assistance under her direction. Draft translations have not received independent bilingual review.

This review inspected related projects for comparison; it did not import their code or datasets. It does not certify the provenance of every earlier line. Any future reuse must record its source and comply with its license. Related-project authors are not collaborators or endorsers of LocaleSafe.

Use this description:

> Created LocaleSafe, an open-source research prototype that tests multilingual service-agent actions and separates language, formatting and workflow failures. Developed its implementation and analysis with AI assistance.

Use “open-source” once the licensed repository is publicly accessible. Before then, use “research prototype.” Do not claim a first-of-its-kind benchmark, independently validated translations, a proven causal language effect or an entirely manually written implementation.

## The contribution we can support

The current contribution is the specific runnable implementation, authored workflow fixtures, archived model outputs, reproducible analyses and documented findings. These are concrete artifacts; their existence does not establish methodological novelty or external impact.

The proposed next contribution is a reviewed permission-and-correction suite and an equal-budget comparison of monitoring approaches, accounting for ordinary model inconsistency. That remains a research direction: novelty, effectiveness and usefulness must be demonstrated. See the [study plan](V1_RESEARCH_PLAN.md).

Credit related work, cite actual results and describe limitations. Authorship of this work does not require claiming ownership of the broader idea.
