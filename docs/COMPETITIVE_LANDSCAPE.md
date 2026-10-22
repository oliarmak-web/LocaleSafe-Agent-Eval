# Related work: where LocaleSafe can add value

**Reviewed October 21, 2026.** This is a targeted landscape review, not an exhaustive novelty certification. Sources are project documentation, author reports and paper abstracts. Absence from an abstract does not establish absence from the full work. Authors' performance claims were not independently reproduced.

## Closest precedents

| Work | What is already covered | Consequence for LocaleSafe |
|---|---|---|
| [LangDrift](https://github.com/RubenGlez/langdrift) | Equivalent multilingual intents, tool/argument correctness, failure categories and CI | A multilingual harness is not a new research method |
| [IndicOrderBench](https://github.com/Lingikaushikreddy/indicorderbench) | Multilingual voice ordering, corrections and committed backend state | Final-action scoring and correction cases are established |
| [BankBench](https://github.com/Sinar/BankBench) | Multilingual banking-agent safety policies | A domain-specific multilingual safety suite alone is insufficient differentiation |
| [MASSIVE-Agents](https://aclanthology.org/2025.findings-emnlp.1099/) | Function calling in 52 languages; localized prompts and example ablations | Adding languages or translating instructions is not enough |
| [Lost in Execution / MLCL](https://arxiv.org/abs/2601.05366) | Multilingual tool failures, parameter-language mismatch and inference-time interventions | Format/argument diagnosis and language-normalization interventions have precedents |
| [Actions Speak Louder than Words](https://arxiv.org/abs/2608.11110) | Cross-language action-policy retention and within-language inconsistency | English rerun controls improve validity; they are not our invention |
| [AURORA](https://aurora.lilt.com/) | Localized agent reliability evaluations across service domains | Multilingual service-agent evaluation already extends beyond isolated tool calls |
| [AuthorizationBench](https://github.com/PEACH-Research-Lab/AuthorizationBench) | Executable authorization contracts, observable actions and resulting state | User authority and task completion must be separated, but that distinction is established |
| [SovereignPA-Bench](https://arxiv.org/abs/2607.05363) | Evolving intent, mid-task updates, permission, deterministic outcomes and user burden | Corrections, consent and unnecessary questions are not individually novel |
| [COAI agent-monitoring report](https://www.coairesearch.org/research/agent-monitoring/report/) | Recorded-action monitors; multilingual permission decisions; history, evidence order and permission changes | A multilingual permission monitor, or evidence-order comparison alone, has close overlap |
| [How Reliable is Multilingual LLM-as-a-Judge?](https://aclanthology.org/2025.findings-emnlp.587/) | Multilingual judgment consistency | Monitor language sensitivity is an established problem |
| [Multilingual Prompt Localization for Agent-as-a-Judge](https://arxiv.org/abs/2604.04532) | Judge-side localization and language-dependent backbone rankings | Varying a judge's language alone is insufficient differentiation |
| [Lower-Resource, Higher Scores](https://arxiv.org/abs/2607.14480) | Language-dependent evaluator scores and acceptance thresholds | Global monitor thresholds and code-switching deserve controls; no first-discovery claim |
| [Authorization Revocation for Long-Running AI Agents](https://arxiv.org/abs/2609.21284) | Revocation under delegation and asynchronous execution | Revoking delegated permission is an existing systems research topic |
| [Agent Memory Is a Surface for Endogenous Authorization Laundering](https://arxiv.org/abs/2609.01836) | Memory-generated false authority and provenance/event-sourcing safeguards | Stale permission in summaries is not an untouched topic |
| [Beyond the Mandate](https://arxiv.org/abs/2608.23858) | Manipulated pre-authorization context in agent payments | Signed transaction data does not settle whether the user intended the action; this issue already has research |

The original [tau-bench repository](https://github.com/sierra-research/tau-bench) also establishes policy-following service workflows and backend-state checks. Its README directs users to its successor for current tasks. LocaleSafe has not run either benchmark; its scores are not comparable leaderboard results.

## Candidate gap, not an established novelty claim

**Which part of a multilingual handoff loses the user's current authority: interpreting the update, preserving it in a summary, acting on it, or judging the action?**

A useful study would cross language switching with permission changes and handoff representation. It would independently score the agent, the permission record and the monitor against a deterministic sandbox. The study combines established methods to investigate a specific failure pathway.

A full-method comparison of the closest authorization, memory and monitor studies remains outstanding, including whether they already cross these factors.

## Scope

Multilingual agent evaluation, authorization checks and language-sensitive monitors have established precedents. LocaleSafe has not audited industry testing practices or validated cultural competence and global deployment. Translated variants remain dependent observations.

## Search record

The earlier [GitHub search](ORIGINALITY_AND_AUTHORSHIP.md) was expanded with web queries including:

```text
multilingual agents consent authorization correction benchmark monitoring language tool calling
agent benchmark stale consent authorization revocation user correction multilingual
multilingual agent monitor evaluator language bias agent judge crossed language benchmark
multilingual agent evaluation false alarms monitor
multilingual agent revocation benchmark
multilingual agent consent handoff benchmark
multilingual agent memory permission benchmark
agent language switch authorization benchmark
```

Only primary technical sources support the comparisons above. Search rankings, snippets and abstracts can miss relevant work. No source code or datasets were imported from these projects. Further review will test the candidate contribution against the closest full methods and artifacts.
