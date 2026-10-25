# Enterprise-sales pilot: understanding the request was not enough

October 23, 2026. **720 recorded model calls; six AI-authored situation templates in five languages. No independent language/domain review or held-out evaluation.** Implementation, cases, translations and analysis used AI assistance.

## What we tested

Two small models assessed a fictional cybersecurity product against a buyer's employee count, data-storage region, identity integration, annual budget and deployment deadline. Five customer-language conditions used the same underlying requirements: English, Brazilian Portuguese, Tamil, Simplified Chinese and Spanish.

Each case was tested under greedy decoding and two seeded sampled repetitions. The model extracted requirements and assessed fit from the conversation, an authored correct requirements record and its own extraction. Product facts and instructions remained English. No sales proposal, CRM write or purchase was executed.

## What we learned about each language

These observations describe the six draft sales situations under greedy decoding. They describe the tested model and prompt setup, not the language or its speakers in general. A complete assessment requires the right fit/escalate decision and the complete list of unmet requirements.

| Language | Observation | What it tells us to investigate |
|---|---|---|
| English | Phi made the right fit/escalate decision in 5/6 cases, but only 4/6 complete assessments. Five English extractions failed strict format because they included Markdown fences. Qwen captured all requirements but completed only 2/6 assessments. | English is a comparison condition, not a guaranteed success. Separate formatting, captured facts and applying product rules. |
| Brazilian Portuguese | Both models captured all six sets of requirements. Phi completed only 1/6 assessments directly, improving to 4/6 with its extracted requirements. | Correctly reading the buyer did not ensure the full conversation produced a sound product-fit assessment. Test the representation passed to the next stage. |
| Tamil | Both models captured all six sets of requirements. Phi made the right fit/escalate decision in 5/6 cases, matching English, but only 1/6 complete assessments. Its extracted requirements improved that to 4/6. | The largest strict-score difference concerned the reasons, not simply choosing fit versus escalation. Check every claimed mismatch. |
| Simplified Chinese | Phi captured 5/6 requirement sets and made the right fit/escalate decision in 4/6 cases, yet none of its complete assessments were correct. Correct structured requirements improved complete assessments to 4/6. | A zero complete score does not mean every request or decision was misunderstood. Correct decisions can come with incorrect reasons. |
| Spanish | Qwen's complete assessment score matched English at 2/6. Phi captured 5/6 requirement sets and made the right decision in 4/6, but completed only 1/6 assessments. Its extracted requirements improved that to 4/6. | Similar-looking language coverage does not establish reliable performance. Evaluate the full decision and its supporting reasons. |

The practical lesson is to **evaluate each deployment language at each stage**, including English. This pilot does not establish that one language needs a different architecture, that Tamil or Chinese is inherently harder, or that language explains every observed difference.

## A concrete sales example

The fictional product costs USD 80,000 annually. A Portuguese buyer allows only USD 60,000; the other requirements are supported. Phi correctly escalated, but incorrectly listed region, integration and deadline as additional mismatches. Qwen also escalated, but added an incorrect deadline mismatch. Both decisions recognized that the sale should not proceed unchanged, but neither assessment explained the actual problem precisely.

In the Chinese integration-mismatch case, Phi escalated for the wrong reason: it named region rather than integration. Qwen instead declared a fit. These are different failure modes, even when a single overall score marks both incorrect. These are archived internal responses, not actual sales advice or sent proposals.

## Findings in plain English

**1. Reading the requirements correctly did not ensure an accurate sales assessment.** Qwen extracted every requirement correctly in all 90 extraction calls. Yet its greedy English fit assessments were fully correct in only 2/6 situations. On all four unsupported English requests it returned an internal fit claim. Errors remained with authored correct requirements, so extraction failure alone cannot explain them. This locates a measured problem in the fit-assessment condition; it does not distinguish model capability from prompt sensitivity.

**2. Response patterns differed across language conditions, but the error type matters.** Phi produced complete correct assessments on 4/6 English situations, 1/6 Portuguese, Tamil and Spanish situations, and 0/6 Chinese situations. However, its fit/escalate decision alone was correct on 5/6 English and Tamil situations and 4/6 in each other language. Much of the strict gap concerns identifying the exact unsupported requirements, not simply saying yes or no. These results do not establish a stable language ranking or verified translation equivalence.

**3. Structured requirements helped some conditions, but were not a complete fix.** Phi's Portuguese and Tamil complete assessments improved from 1/6 with conversations to 4/6 with correct structured requirements. Qwen remained at 2/6 with those records. A generated extraction also gave Phi 4/6 in Portuguese and Tamil, both of which had 6/6 valid and exact greedy extractions. Accurate extraction and downstream decision quality must be measured separately.

**4. Format compliance can make English look worse at extraction.** Five of Phi's six greedy English extraction responses were wrapped in Markdown and failed the strict JSON contract. Its Portuguese and Tamil extractions were all valid and exact. The low English extraction score is not sufficient evidence of poor English comprehension. The original replies and their downstream use remain unchanged; no format repair was performed.

**5. Ordinary inconsistency remains relevant.** Between Phi's two sampled repetitions, complete assessment correctness changed on 2/6 English conversation situations and on 2/6 in every non-English language. Qwen's sampled correctness did not change between those two repetitions, although it had a low assessment baseline. Two samples do not characterize the full response distribution. Matched language comparisons must be read alongside these repeats.

## What this means for a sales-agent team

Score requirement capture, evidence-based product fit, decision correctness, the reasons for escalation, format compliance and unnecessary refusal separately. Otherwise a model can correctly repeat a requirement and still endorse an unsuitable product—or escalate for the wrong reason.

Do not call this proof of lost revenue or a production safety failure. These are simulated internal assessments under one frozen prompt setup. A stronger test needs independently reviewed and native-authored buyer requests, more realistic product documents, additional situation families, capable-model screening, controlled prompt variants and untouched evaluation cases. Customer language, document language, business geography and regulatory rules must remain separate factors.

## Inspect and reproduce the analysis

Python 3.11+, no model dependencies or API keys for replay:

```sh
python -m experiments.summarize_sales_pilot experiments/results/sales-qwen3-4b-20261023 experiments/results/sales-phi4-mini-20261023 --output-dir reports/sales-reproduction
```

Choose a new output directory. This audits recorded calls and regenerates tables; it does not generate fresh model responses. Prompt render hashes remain recorded; native-template regeneration requires the pinned tokenizer. [Full results](SALES_PILOT_RESULTS.md) · [Protocol](../experiments/sales-pilot/PROTOCOL.md) · [Execution history](../experiments/sales-pilot/EXECUTION_HISTORY.md) · [Machine-readable analysis](../experiments/analysis/sales-pilot/summary.json).
