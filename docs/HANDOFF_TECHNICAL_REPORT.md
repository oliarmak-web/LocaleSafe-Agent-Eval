# Multilingual permission handoffs: separating language, record contracts and monitor errors

Olivia Iarmak · LocaleSafe · October 22, 2026

**Development research report.** Implementation, draft translations, analysis and writing used AI assistance. No independent bilingual review or peer-reviewed validation has been completed. [Contribution record](../CREDITS.md).

## Abstract

We test whether changing conversation language, summarizing user instructions or changing evidence format affects permission-sensitive service-agent behavior. We recorded 2,880 calls covering summaries, actor actions and fixed-action monitor judgments, followed by 384 exploratory monitor-intervention calls. Qwen3-4B passed the predefined development competence screen; SmolLM3-3B did not and was excluded from the evaluation split. In greedy development runs, Qwen selected the correct action on all 32 full-history cases but only 23 generated-record cases. Its generated records preserved the current permission field in all 192 outputs across development and evaluation, while requested-action representation and monitor judgments still failed. An explicit-rule monitor prompt reduced forbidden-action acceptance but increased false blocking and lowered total accuracy. These results favor component-level workflow diagnosis over a simple language-deficit explanation in this bounded setup.

## 1. Research question

When a user withdraws or changes permission across a language switch, where does the failure occur: interpretation, handoff representation, action selection or monitor judgment?

The experiment separates task correctness from permission. A wrong proposal may be permitted but fail the task; a correct authorized change may be blocked by a monitor. All executable actions pass through the same trusted permission guard.

## 2. Methods

The dataset has eight authored templates, two identifier/value variants and four language patterns: en-en, es-es, en-es and es-en. Four templates form the development split and four different templates form the evaluation split. The 64 rows are related observations, not 64 independent situations. Spanish wording is unreviewed.

Each model first processes 32 development rows under greedy decoding and two sampled repeats. For every case/profile it generates an English narrative and a structured record, then selects actions from full history, the narrative, the generated record and the oracle record. Fixed permitted and forbidden actions are judged separately from full history and generated records. The same model performs all roles within its run.

The oracle is a deliberate perfect-extraction control. When records match, oracle and generated-record actor prompts have identical instructions and representation. The full-history projection excludes reference labels; generated summaries are retained unchanged. Monitor actions are fixed independently of actor outputs.

The English gate required at least 7/8 correct greedy en-en actions in both full-history and oracle-record development conditions. Qwen scored 8/8 in each; SmolLM3 scored 6/8 and 4/8. Only Qwen proceeded to the reserved templates. There, its full-history English score fell to 6/8, underscoring the limited generalization of the development screen.

Collection used pinned Qwen3-4B and SmolLM3-3B revisions on a free Colab Tesla T4, float16 without quantization, Python 3.13.15, PyTorch 2.11.0+cu130 and Transformers 4.57.6. Thinking was disabled. Sampled profiles used temperature 0.7, top-p 0.8 and top-k 20; greedy was reported separately. The protocol and source were frozen before initial collection. [Full protocol](../experiments/handoff-study/PROTOCOL.md).

## 3. Results

| Qwen3-4B greedy actor condition | Development | Evaluation |
|---|---:|---:|
| Full history | 32/32 | 26/32 |
| Oracle record | 32/32 | 32/32 |
| Generated record | 23/32 | 20/32 |
| Generated text | 29/32 | 20/32 |

**Language switching was not uniformly worse.** All four development language patterns scored 8/8 with full history. On evaluation templates, en-es scored 8/8 and each other pattern 6/8. This does not establish equivalence or language superiority; it contradicts a simple, consistent switch penalty in these cases.

**Permission fidelity alone missed downstream failures.** Qwen preserved permission, version and source fields in every generated record across both splits and all decoding profiles. Exact-record fidelity was 20/96 in development and 0/96 in evaluation. The requested action was often a string such as `"commit"` rather than the required tool-call object. These are contract and action-representation failures, not evidence that permission was always lost.

**The monitor depended on its evidence.** With full history, Qwen's greedy monitor had zero false allows in either split but falsely blocked 20/32 permitted evaluation probes. With generated records, it falsely allowed 15/32 forbidden development probes and 24/32 evaluation probes.

All outputs, invalids, sampled-repeat results, field-level scores and denominators are available in the [generated result tables](HANDOFF_RESULTS.md) and [machine-readable analysis](../experiments/analysis/handoff/summary.json).

## 4. Exploratory interventions

After inspecting these results, we tested 128 fixed probes under three monitor conditions: exact baseline repeat, an explicit permission-rule paragraph, and oracle records. The baseline reproduced all original greedy verdicts. Explicit rules reduced false allows from 39/64 to 18/64 but introduced 40/64 false blocks on permitted probes; total accuracy fell from 89/128 to 70/128. Oracle records yielded 128/128 correct judgments. The full reference record changes action representation and content; this does not identify the single decisive field. [Follow-up results](MONITOR_FOLLOWUP.md).

A separate post-hoc routing replay validates generated-record shape and selects an already recorded full-history actor output when validation fails. Qwen's greedy correctness changes from 23/32 to 32/32 on development and 20/32 to 26/32 on evaluation. SmolLM3's second sampled profile worsens from 19/32 to 17/32. This replay makes no new model calls and does not establish a deployed routing improvement. Structural validity also does not authenticate claimed permission. [Routing results](../experiments/analysis/handoff/routing.json).

## 5. Contribution and prior work

The contribution is this matched bilingual experiment record and its separation of permission fidelity, action-contract compliance and monitor errors. It is not a first multilingual benchmark or a new authorization primitive.

[EAL-Bench](https://arxiv.org/html/2609.01836v1) already separates memory formation and action propagation, with typed/text memory and faithful-record controls. [MasDrift](https://arxiv.org/html/2608.07556v3) studies authorization across multi-agent architectures. [COAI's monitoring study](https://www.coairesearch.org/research/agent-monitoring/report/) compares recorded-trajectory monitors across language/evidence conditions. LocaleSafe holds a bounded workflow fixed and crosses conversation language, handoff representation and fixed-action monitor evidence. [Method comparison](HANDOFF_METHOD_COMPARISON.md).

## 6. Limitations and reproducibility

Eight templates, draft translations and only one model passing the competence screen limit conclusions. The evaluation split is family-separated but not contamination-resistant. Cross-family role combinations, autonomous tool loops, real services, distributed revocation and speech are not tested. Narrative summaries lack independent semantic review. The monitor intervention and routing replay are post-hoc; neither source split is held out for those analyses. No significance, population failure rate or production safety claim is supported.

The new work contains 576 summary calls, 1,152 actor calls and 1,536 monitor calls: 3,264 total. Cached routing adds zero calls. Earlier LocaleSafe studies are separate. The archives preserve prompts, responses, settings, source snapshots and hashes; auditors reconstruct prompts, dependencies, seeds and scores. [Execution provenance](../experiments/handoff-study/EXECUTION_HISTORY.md) · [Independent review procedure](../experiments/handoff-study/REVIEW.md).

For software citation use [CITATION.cff](../CITATION.cff) or [BibTeX](../CITATION.bib), identifying the exact commit and experiment. This repository report has no journal publication or assigned DOI.
