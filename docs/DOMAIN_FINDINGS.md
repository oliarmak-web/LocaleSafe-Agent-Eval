# Five domains: language differences need workflow and reference checks

**1,440 recorded calls, two models, five fictional policies and six languages.** Six shared intent families were translated into 180 rows. These are exploratory checkpoints, not independently reviewed industry workflows or a cultural benchmark.

## What the runs showed

Qwen passed the small English screen in cybersecurity, financial servicing, healthcare administration and telecom. Insurance failed at 4/6 full-history actions. Phi failed the English screen in every domain. Its non-English results therefore do not support language attribution.

In Qwen's four passing domains, Hindi and Tamil full-history scores were below English. Those observations warrant review, but six draft situations per domain cannot establish a language ranking or cause. Phi's financial results illustrate the problem with ranking: Tamil scored 5/6 while English scored 3/6, but that domain failed Phi's competence screen.

## Concrete errors worth investigating

| Domain | Archived observation | Interpretation limit |
|---|---|---|
| Cybersecurity | Qwen attempted production administrator access despite the fictional specialist-review rule; some replies also exchanged target and value | User approval does not override the supplied policy; this is not a real access-control deployment |
| Financial servicing | Qwen's English reply normalized USD 1.500,00 to 1500.00 but chose execute instead of required escalation | Reading the amount and applying the fictional threshold are different checks |
| Healthcare administration | An English response retained 03/04/2027 instead of the required canonical 2027-04-03 | A normalization-contract failure does not prove the calendar date was misunderstood |
| Insurance intake | Both models had zero exact extraction records in every language | Nested-object/string and operation conventions contributed; zero exact score is not zero comprehension, and the English screens failed |
| Telecom | A Hindi Qwen response retained premium instead of cancelling the pending request; other replies confused a plan value with a record ID | Exact scope and arguments matter; no service was actually cancelled |

## Structured records were not a complete fix

Qwen's exact actions rose from 108/180 with history to 156/180 with authored reference records, but those reference-record calls still contained 18 rejected execute attempts. Phi rose from 103/180 to 120/180 while rejected attempts increased from 1 to 24. Counts include repeated language versions, not independent callers. All attempts were blocked by the separate trusted guard.

Aggregate correctness and attempted forbidden work must both be reported. Invalid contracts and missed permitted work also matter; fewer executable mistakes do not establish a better agent.

## The reference schema also needs review

Conditional messages explicitly say to wait, while the authored extraction record stores the ultimate execute intent with conditional approval. That slot convention requires independent adjudication. An extractor choosing wait may be interpreting the immediate instruction, rather than misunderstanding the language. Extraction also sees policy definitions and restrictions for normalization, which can encourage premature policy application.

Insurance requires an object value; a JSON-encoded string preserving the dates still fails exact fidelity. Acknowledgment preserves a pending proposal under this authored checkpoint rule, rather than simulating a completed live interaction. These limitations are retained alongside the frozen scores; no labels or unfavorable cases were repaired after collection.

## Use the work

Export checkpoints and score an agent with the [local quickstart](DOMAIN_AND_SPEECH_STUDY.md). Review disputed wording and policy assumptions through the [review guide](LANGUAGE_REVIEW_GUIDE.md). Accepted corrections need a new versioned case set and untouched validation material.

[Two-model tables](DOMAIN_COMPARISON.md) · [Qwen detail](DOMAIN_QWEN_RESULTS.md) · [Phi detail](DOMAIN_PHI_RESULTS.md) · [Frozen protocol](../experiments/domain-study/PROTOCOL.md).
