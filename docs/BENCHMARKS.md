# What is actually evaluated?

## Registry and status

| Suite / benchmark | Status in this repository | Purpose and limits |
|---|---|---|
| LocaleSafe custom scenario suite, draft v0.1 | Implemented; 18 fixture cases and a 54-case local-model pilot | Six paired scenario families; illustrative escalation, clarification, and exact proposed tool calls. Not an established or independently validated benchmark. |
| Synthetic perfect / injected-failure fixtures | Run as engineering controls | Verify the scorer and failure handling; not model performance evidence. |
| Strict JSON contract | Applied to pilot outputs | Integration/format compliance; not itself language understanding or safety. |
| Fence-only parsing diagnostic | Post-hoc analysis of the same pilot outputs | Separate Markdown wrapping from content errors. No new inference or independent experiment. |
| Paired English reference analysis | Implemented descriptive analysis | English-correct/other-wrong, reverse disagreements, shared failures, and unparseable pairs. Language-associated differences are not proof of causation. |
| [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) | Not run; no adapter implemented | External function-calling reference. Uses its own datasets and evaluators; LocaleSafe JSON exact match is not BFCL AST accuracy. |
| [MASSIVE-Agents](https://aclanthology.org/2025.findings-emnlp.1099/) | Not run; candidate external multilingual validation | Published multilingual function-calling benchmark across 52 languages. Check data license, exact release, supported-language overlap, schema, and evaluator before importing/running. |
| [Ticket-Bench](https://arxiv.org/abs/2509.14477) | Related work only; not run | Multilingual/localized soccer-ticket task benchmark. Different domain and localization; not a direct airport safety comparator. |
| [MLCL / Lost in Execution](https://arxiv.org/abs/2601.05366) | Related work only; not run | Existing diagnostic multilingual tool-call benchmark separating execution conventions from semantic failures; direct overlap with attribution motivation. |

No external leaderboard score, clinical validation, audio/ASR score, hallucination detection score, or general fairness score has been measured by this repository. Do not present an external benchmark as completed merely because it is cited here. Pin external releases and publish exact subsets, prompts, model revision, evaluator version, license/provenance, and artifacts when an integration is added.

See the [authored research agenda](AUTHORED_RESEARCH_AGENDA.md) for a proposed U.S. service-workflow suite, use cases, detailed task families, scorecards, controls, and publication/authorship milestones. This proposed v2 suite is not implemented or validated yet.

## Metrics versus benchmarks

A benchmark is a defined task/dataset/evaluation protocol. A metric is a calculation on its outcomes. Current metrics are exact decision correctness, exact call/argument correctness, invalid output count, missed/unnecessary escalation under the illustrative policy, and paired pass-rate differences. These do not measure internal reasoning, clinical correctness, broad hallucinations, or societal bias.

## Is language actually the problem?

The pilot cannot establish that yet. A low end-to-end score could come from the agent prompt, weak general model capability, translation problems, output formatting, tool argument handling, or language interpretation. The extra-check prompt changes instructions and therefore tests an interaction with the workflow; it is not a pure language intervention.

The diagnostic separates:

1. **Format failure:** no valid output object. Decision/tool correctness remains unknown; do not invent an observed bad decision.
2. **Decision error:** a parseable choice disagrees with the fixed policy.
3. **Tool error:** a parseable proposal uses wrong calls or arguments. This can overlap with a decision error; the categories are not additive.
4. **Paired outcome:** compare each non-English item to its matching English scenario under the same model/prompt. Shared failures suggest a general task/integration weakness to investigate. English-pass/other-fail is a language-associated counterexample, not proof that language caused it. Reverse differences must also be reported.

Both strict and explicitly post-hoc fence-only parsing are retained. Decision comparisons exclude pairs with unparseable outputs and report that denominator. Exclusion can be language-dependent, so these conditional comparisons are exploratory, not an unbiased estimate of language effects.

## Stronger identification study — next gate

- Have qualified reviewers independently check semantic equivalence, urgency, negation, location, and policy labels; adjudicate disagreement. Keep translation uncertainty visible.
- Add multiple English paraphrases and multiple translations per scenario, separating within-language phrasing sensitivity from between-language differences.
- Freeze many new held-out scenario families; keep all versions of a family in one split. Choose sample sizes and repeated generations from a pilot-based precision/power rationale.
- Hold model, tool schema, task semantics, decoding, and parser fixed; cross language with prompt condition and repeat seeds. Do not pool repeated generations as independent scenarios.
- Use an independently tested canonical tool simulator. First test it with perfect structured decisions. Run the same structured decisions through it for every language: any difference there is a workflow bug, not model language comprehension.
- Compare unconstrained output with a separately specified grammar/schema-constrained condition; do not quietly repair one language's outputs or discard its failures.
- Evaluate native tool calls and later clarification dialogues separately from JSON text generation. Separate ASR later by giving the same agent reference versus recognized transcripts.
- Report stage-specific outcomes, paired discordances in both directions, family-level uncertainty, and negative findings. Use external benchmark validation alongside custom domain scenarios rather than replacing either with the other.
