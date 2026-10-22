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

## What we learned

**The clearest failures in this study involved handoffs and permission checks. We did not find a consistent penalty for switching between English and Spanish.** That does not establish that language is harmless: the cases are small, and only one model passed the initial English screen.

1. **A wrong action is not automatically a language failure.** With the full conversation, Qwen3-4B chose the correct action in all 32 development cases. On the separate evaluation cases, it scored 6/8 in English only, 6/8 in Spanish only, 8/8 switching from English to Spanish and 6/8 switching in the other direction. Switching languages was not consistently harder here. Compare against English failures before attributing a gap to language.

2. **Keeping the permission field correct is not enough.** Qwen preserved permission in all 192 generated structured summaries, yet its development action score fell from 32/32 with the full conversation to 23/32 with a generated summary. Many summaries described the requested action in the wrong format. A handoff needs checks on the complete record and the action it produces; checking one field misses failures. We have not isolated which record changes caused each error.

3. **A stricter safety prompt can block legitimate work.** In a follow-up, added rules reduced approvals of forbidden actions from 39/64 to 18/64. But rejections of permitted actions rose from 0/64 to 40/64. Overall correctness fell from 89/128 to 70/128. Count both unsafe approvals and unnecessary refusals before calling a monitor better.

4. **Better evidence helped the monitor in these cases.** When supplied with the authored correct record, the monitor judged all 128 follow-up actions correctly. This is a diagnostic control: it shows what the model could do with perfect input. Automatically producing that input remains unsolved in this study.

### Why this matters for agent builders

A customer may approve an appointment change in English and withdraw permission in Spanish. To investigate a wrong booking, test the original conversation, the handoff summary, the proposed action and the permission monitor separately. LocaleSafe provides those comparisons so teams can identify where to investigate before choosing a fix.

**Multilingual evaluation is useful, but a language leaderboard alone cannot explain these failures.** Test matched requests within and across languages, verify that the model can do the English task, and measure whether summaries and monitors preserve the user's latest permission. These experiments support that evaluation approach; they do not establish how common these failures are in deployed systems.

### What the evidence covers

**3,264 model calls:** 576 summary generations, 1,152 action decisions and 1,536 monitor judgments. These are repeated measurements on **64 draft English/Spanish cases across eight templates**, not 3,264 independent situations. The study separates development and evaluation situation families and includes deterministic and sampled responses. The action counts above use deterministic responses; the 192-record check includes all three decoding settings.

Qwen3-4B passed the initial English task screen. SmolLM3-3B failed it, so its evaluation run was skipped. The monitor-rule follow-up and replay of a fallback strategy were designed after inspecting the initial results. Translations lack independent bilingual review. These results do not establish causal language bias, a stable language ranking or production safety. Zero unauthorized sandbox changes reflect a separate code-level permission guard, not perfect model behavior.

[Technical report and plain-English interpretation](docs/HANDOFF_TECHNICAL_REPORT.md) · [Complete result tables](docs/HANDOFF_RESULTS.md) · [Monitor intervention](docs/MONITOR_FOLLOWUP.md) · [Protocol](experiments/handoff-study/PROTOCOL.md).

## Additional models: the output contract is another failure source

We ran **1,920 additional development calls** on Mistral-7B-Instruct-v0.3 and Phi-4-mini-instruct. Neither passed the unchanged English screen, so neither proceeded to evaluation:

| Model | English with full conversation | English with perfect reference record |
|---|---:|---:|
| Mistral-7B-Instruct-v0.3 | 0/8 | 1/8 |
| Phi-4-mini-instruct | 4/8 | 8/8 |

**These are exact command-contract scores, not measures of general intelligence or language comprehension.** Mistral sometimes added a word before its JSON command; Phi sometimes wrapped JSON in Markdown. The frozen scorer rejects both. All 96 Phi structured summaries failed strict parsing, which makes their field scores zero; that does not show every permission fact was misunderstood. We preserved the raw answers without repairing them.

Phi's greedy action score improved from 15/32 with the full conversation to 32/32 with perfect reference records. This gives another reason to investigate the input representation and output contract before blaming language. It does not reproduce Qwen's evaluation result or establish a language effect. Across this study and follow-up, **5,184 calls** are now archived; only Qwen qualified for evaluation.

[Additional model results](docs/MODEL_EXTENSION_RESULTS.md) · [Replication protocol](experiments/handoff-study/MODEL_EXTENSION.md).

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
