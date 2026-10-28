# LocaleSafe

**Find out why a multilingual AI agent took the wrong action.**

LocaleSafe tests whether service agents preserve a customer's request, follow the supplied policy and act only with current permission. Compare the original conversation, an agent-generated summary and an authored correct record to investigate language, workflow, handoff and monitor failures.

Created and maintained by **Olivia Iarmak**. MIT-licensed research prototype. Implementation, translations and documentation use AI assistance.

## What you can test

| Workflow | Failure to investigate |
|---|---|
| Cybersecurity access | Granting production administrator access despite a specialist-review rule |
| Financial servicing | Reading an amount correctly but executing a payment that requires review |
| Healthcare scheduling | Losing a corrected visit date or accepting an unverified proxy's instructions |
| Insurance intake | Confusing the incident date with the reporting date |
| Telecom account changes | Cancelling an active service instead of a pending plan change |
| Enterprise product fit | Capturing buyer requirements but inventing capabilities or giving incorrect escalation reasons |
| Agent handoffs | Acting on an old instruction after approval changes or is withdrawn |

The five-domain suite covers **English, Spanish, Hindi, Brazilian Portuguese, Simplified Chinese and Tamil**. Sales and handoff studies use separate language sets and task contracts. Policies and records are fictional; no command changes a real account, sends a message or moves money.

Earlier booking fixtures use a fictional service-visit record with a date. If the user replaces an approved April 12 date with April 19, the agent must update that record to April 19 and leave other bookings alone. They test dates, record selection and approval, rather than availability search or a complete scheduling service.

## Main findings

- **Language is one possible failure source.** In 1,440 five-domain calls, Qwen passed four small English task screens; insurance failed. Phi failed all five. Hindi and Tamil gaps in Qwen's passing domains warrant investigation, but the draft cases cannot establish language as the cause.
- **Correct facts do not guarantee correct actions.** Qwen read a financial amount correctly but chose execution instead of required review. In the separate sales pilot, it captured every requirement in 90 extraction calls yet scored only 2/6 complete greedy English assessments.
- **A handoff can introduce errors.** Qwen's development action score fell from 32/32 with full history to 23/32 with generated structured summaries, despite preserving every permission field. Added monitor rules reduced unsafe approvals but also blocked more permitted work.
- **Formatting can distort conclusions.** Changing only tool-example presentation raised Mistral's full-history score from 0/32 to 32/32. The change hurt other conditions; valid JSON was not a safety guarantee.
- **The speech evidence is separate.** Forty local Whisper-small transcriptions of 20 public clips were identical with automatic and supplied language labels. MINDS references are ASR hypotheses, so disagreement with them is not verified recognition error. These clips do not test the domain workflows or commercial voice products.

These are exploratory results on small, AI-assisted draft fixtures. Call counts include repeated conditions and translations, not independent situations. Reference conventions, output contracts and weak English task performance constrain interpretation. Independent language/domain review remains outstanding. The studies do not establish cultural effects, stable language rankings or production safety. Guarded sandbox outcomes are separate from model behavior.

**[Research index: findings, tables, protocols and evidence](docs/RESEARCH_INDEX.md)**

## Start here: reproduce the main experiment locally

Use Git and Python 3.11+. This audit uses only Python's standard library: no API key, model download or GPU. Cloning needs network access and, while the repository is private, authorized GitHub access.

```sh
git clone https://github.com/oliarmak-web/LocaleSafe-AI-Agentic-Demo.git
cd LocaleSafe-AI-Agentic-Demo
python -m experiments.summarize_domain_comparison experiments/results/domain-study-qwen3-4b-20261027 experiments/results/domain-study-phi4-mini-20261027 --output-dir reports/domain-replay
```

This verifies both five-domain archives and rebuilds `comparison.json` and `RESULTS.md` from **1,440 recorded calls**. Expect Qwen to pass four English domain screens and Phi to pass none. It recomputes existing results; it does not generate new model answers. Choose a new output directory when repeating a run.

**[Reproduction guide: other studies, permission demo and your own agent](docs/QUICKSTART.md)**

## What this project contributes

**LocaleSafe gives agent builders a reproducible way to investigate a costly ambiguity: did the agent misunderstand the customer's language, lose an instruction during handoff, misapply a policy or receive the wrong safety judgment?** Those failures call for different fixes. A single task-success score cannot distinguish them.

- **Diagnostics across five service domains.** Authored checkpoints cover access permissions, payment review, scheduling, insurance records and telecom changes in six languages. Fixed task details let teams compare language conditions while checking English task competence first.
- **Evidence that fluent understanding can still lead to forbidden actions.** Recorded experiments separate captured facts from decisions and tool arguments: an agent can read an amount correctly yet ignore a review requirement. Builders can test both stages before choosing a mitigation.
- **Tests of safety trade-offs.** Handoff and monitor experiments measure unsafe approvals alongside unnecessary refusals. They expose interventions that improve one score while preventing legitimate work or worsening another condition.
- **Reusable evaluation infrastructure.** Teams can export checkpoints, score their own agent's untouched replies and audit the published findings from prompts, raw outputs, source snapshots and hashes. Failed attempts and negative results remain available for independent scrutiny.

For teams building multilingual agents that can change customer records, this supports targeted debugging, evaluation design and regression checks across languages. The contribution is the authored diagnostic suite, empirical failure analyses and reproducible tooling. Industry adoption, independent validation and production impact remain to be demonstrated; the research index documents the evidence, related work and limits.

## Contribute and cite

Independent language/domain review, new situation families, model adapters and independent reproductions are welcome. **[Contribution guide](CONTRIBUTING.md)**. Keep credentials and private customer data out of contributions.

If you use the code, fixtures or analyses, cite **Olivia Iarmak, LocaleSafe**, with the exact experiment and commit. **[Citation metadata](CITATION.cff)**. Cite external models and datasets separately; no DOI or peer-reviewed validation is claimed.
