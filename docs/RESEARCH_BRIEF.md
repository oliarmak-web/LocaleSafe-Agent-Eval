# LocaleSafe: research brief

**Research prototype · Updated October 27, 2026.**

## In one sentence

LocaleSafe tests whether multilingual service agents choose the right action, preserve the user's current permission and receive the right judgment from a safety monitor.

## Who created it?

Olivia Iarmak created LocaleSafe and directs its development. Implementation, translations, analysis tooling and writing use AI assistance. [Contribution record](../CREDITS.md).

## What is the problem?

An agent can speak the user's language yet act on the wrong record. A later correction can be lost in a handoff. A monitor can then allow the wrong action or block a valid one. Teams need to distinguish those failures before deciding whether to change the language handling, workflow or safeguards.

Illustrative uses include appointment changes, customer-service updates and interpreter handoff. These are potential applications, not verified deployments. Language does not determine nationality, region or date convention.

## What evidence exists?

- The initial handoff study recorded 2,880 initial calls across two model families and 384 exploratory monitor calls. Qwen passed the development English screen; SmolLM3 did not and was not run on evaluation families.
- Qwen's greedy action accuracy fell from 32/32 with full history to 23/32 with generated structured records on development cases. Permission fields were preserved; requested-action representation and downstream judgment still failed.
- Explicit monitor rules reduced forbidden-action acceptance but increased blocking of permitted actions. Perfect reference records yielded 128/128 correct monitor judgments in the follow-up. This is an oracle result, not a deployed fix.

- A completed development study recorded 1,800 decisions from Qwen3-0.6B and Qwen3-1.7B across five languages. In the larger model's baseline, 278/300 commands were validly formatted, but 37/300 were correct.
- Translating that model's instructions gained six successes and lost eleven on matched non-English requests.
- A post-hoc repeatability analysis found that one of eleven successful English baseline outputs failed on the English rerun, versus four to nine failures on matched other-language outputs. These overlapping comparisons reuse English anchors.
- The earlier 48-row handoff prototype remains a separate synthetic control set.

Sources: [handoff report](HANDOFF_TECHNICAL_REPORT.md), [monitor follow-up](MONITOR_FOLLOWUP.md), [earlier workflow study](WORKFLOW_STUDY.md) and [rerun analysis](CONSISTENCY_CONTROL.md). Synthetic controls and model studies are separate evidence sets.

## What did the newer experiments add?

- **Output format can confound a failure score.** In 256 exploratory Mistral/Phi calls, changing tool examples to JSON-only objects improved Mistral's full-history actions from 0/32 to 32/32. The same change caused nine Phi reference-record regressions. Valid JSON alone did not ensure authorized actions. [Format follow-up](FORMAT_FOLLOWUP.md).
- **Reading a buyer's requirements is different from applying product facts.** A separate 720-call cybersecurity-sales pilot tested English, Brazilian Portuguese, Tamil, Simplified Chinese and Spanish. Qwen extracted requirements correctly in all 90 extraction calls, yet completed only 2/6 greedy English assessments correctly. Phi's Tamil fit/escalate decisions matched English at 5/6, while complete assessments scored 1/6 versus 4/6 because the stated mismatches were wrong. These six draft situations do not support a language ranking. [Language-by-language findings](SALES_PILOT_FINDINGS.md).
- **An executor needs both permission checks and retry protection.** In 21 injected SQLite controls, current-approval checks plus deduplication prevented unapproved and duplicate effects, but two corrected requests still required replanning. These are engineering controls with no model calls. [Order controls](ORDER_CONTROLS.md).

## What is the contribution?

The deliverables are a runnable diagnostic toolkit, authored workflow fixtures, archived model outputs and reproducible analyses. The latest study distinguishes permission-field accuracy, action-contract compliance and monitor judgment rather than assuming that language or permission loss explains every error.

The project builds on existing multilingual, authorization and monitoring research. Its empirical findings remain exploratory; wider significance has not been established. [Methods comparison](HANDOFF_METHOD_COMPARISON.md).

## Scope and limitations

The studies are exploratory and use draft translations. They do not establish causal language effects or production safety. Speech, clinical correctness, hallucination rates and industry-wide failure prevalence are outside scope. Only one model passed the handoff study's competence screen; independent bilingual review remains outstanding.

## Citation

Olivia Iarmak. *LocaleSafe: diagnose language and workflow failures in service agents*. Software repository, 2026. Include the exact commit and experiment used. [CITATION.cff](../CITATION.cff) · [BibTeX](../CITATION.bib).

No DOI or journal publication is currently assigned.
