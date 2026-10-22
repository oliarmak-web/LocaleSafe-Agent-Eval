# LocaleSafe: research brief

**Research prototype · October 21, 2026.**

## In one sentence

LocaleSafe tests whether multilingual service agents choose the right action, preserve the user's current permission and receive the right judgment from a safety monitor.

## Who created it?

Olivia Iarmak created LocaleSafe and directs its development. Implementation, translations, analysis tooling and writing use AI assistance. [Contribution record](../CREDITS.md).

## What is the problem?

An agent can speak the user's language yet act on the wrong record. A later correction can be lost in a handoff. A monitor can then allow the wrong action or block a valid one. Teams need to distinguish those failures before deciding whether to change the language handling, workflow or safeguards.

Illustrative uses include appointment changes, customer-service updates and interpreter handoff. These are potential applications, not verified deployments. Language does not determine nationality, region or date convention.

## What evidence exists?

- A completed development study recorded 1,800 decisions from Qwen3-0.6B and Qwen3-1.7B across five languages. In the larger model's baseline, 278/300 commands were validly formatted, but 37/300 were correct.
- Translating that model's instructions gained six successes and lost eleven on matched non-English requests.
- A post-hoc repeatability analysis found that one of eleven successful English baseline outputs failed on the English rerun, versus four to nine failures on matched other-language outputs. These overlapping comparisons reuse English anchors.
- A separate handoff prototype contains 48 draft English/Spanish rows and five injected-failure controls. It has not been tested with real models.

Sources: [workflow study](WORKFLOW_STUDY.md), [rerun analysis](CONSISTENCY_CONTROL.md), [handoff protocol](../experiments/handoff/PROTOCOL.md). The model study and synthetic handoff controls are separate evidence sets.

## What is the contribution?

The current deliverables are a runnable diagnostic toolkit, authored workflow fixtures, an archived experiment record and reproducible analyses. The next empirical question is where the latest permission is lost across language switches and handoffs, and whether an explicit permission record helps without blocking valid actions.

The project builds on existing multilingual, authorization and monitoring research. Its specific handoff study is under development; uniqueness and wider significance have not been established. [Comparison with related work](COMPETITIVE_LANDSCAPE.md).

## Scope and limitations

The studies are exploratory and use draft translations. They do not establish causal language effects or production safety. Speech, clinical correctness, hallucination rates and industry-wide failure prevalence are outside scope. The handoff study has not yet run with real models.

## Citation

Olivia Iarmak. *LocaleSafe: diagnose language and workflow failures in service agents*. Software repository, 2026. Include the exact commit and experiment used. [CITATION.cff](../CITATION.cff) · [BibTeX](../CITATION.bib).

No DOI or journal publication is currently assigned.
