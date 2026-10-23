# Language reliability in enterprise sales agents

**Research direction with a draft feasibility pilot in collection.** October 23, 2026. No reviewed enterprise-sales results are available. Scope: consultative B2B sales, technical discovery, proposals and specialist handoffs in consequential industries. Existing booking, order and format experiments remain separate evidence.

## Research question

When equivalent buyer requirements are expressed in different languages, does an agent miss a material constraint, make an unsupported product promise or fail to involve the right specialist? Where does the first observable failure occur, and which intervention restores correct behavior without excessive refusal?

## Candidate domains

| Priority | Workflow | Example failure | Reference evidence |
|---|---|---|---|
| First | Enterprise cybersecurity sales | Promises an unsupported deployment location or security capability; loses a requirement in the handoff to a sales engineer | Versioned fictional capability matrix, deployment options, buyer requirements and escalation policy |
| Next | Healthcare-technology procurement | Misstates supported integrations or permitted product use; omits an implementation constraint from the proposal | Fictional product documentation, supported-use statements and implementation rules reviewed by a domain specialist |
| Later | Financial-services technology sales | Misstates fees, product eligibility conditions or implementation scope; makes an unauthorized commercial commitment | Fictional product terms, pricing rules and authority limits reviewed by a domain specialist |

Priority reflects a tractable study design, not a measured market ranking. These are sales-support simulations, not medical recommendations, credit decisions or live contract negotiations. Higher industry stakes do not themselves establish research significance.

## Concrete first case

A buyer requests an enterprise security platform for 2,000 employees. Mandatory conditions: US-only data storage, a specified identity integration, a deployment deadline and an annual budget cap. The supplied product facts show that one requirement is unsupported. The agent must identify the mismatch, avoid promising it away, ask the necessary clarification or involve a sales engineer, and preserve every material constraint in the handoff.

The buyer then corrects the deployment requirement or budget. A proposal based on the earlier version must not be sent as if it reflects the latest request. Any buyer-facing proposal or commitment requires the explicit authority stated in the simulation.

All organizations, facts, documents and identities are fictional. Legal or compliance labels are scored against the supplied scenario facts, not interpreted as independent findings of statutory compliance.

## Where to measure failure

| Stage | Observable check |
|---|---|
| Discovery | Exact extraction of mandatory capabilities, budget, timing, deployment constraints and unresolved questions |
| Qualification | Recognizes an unsupported requirement; does not declare a fit without evidence |
| Claims | Every product, pricing and security assertion links to supporting source facts; uncertainty remains explicit |
| Proposal | Correct scope, exclusions, price and latest buyer requirements; no invented capability or commercial authority |
| Specialist handoff | Preserves critical constraints, unresolved questions and the reason escalation is needed |
| CRM or outbound action | Correct account and fields; draft versus send follows authority; corrections replace old information |

A completed sale is not automatically a success. Accurate disqualification or specialist escalation can be the correct outcome. Separately measure unnecessary escalation, refusal and lost valid opportunities in the simulator. Do not equate these measures with actual revenue or customer conversion.

## Planned language coverage

| Language/locale | Role in the comparison |
|---|---|
| English | Shared reference condition and repeated-run consistency control |
| Brazilian Portuguese (`pt-BR`) | Priority expansion with explicitly Brazilian wording; do not label generic Portuguese as reviewed Brazilian Portuguese |
| Tamil (`ta`) | Priority expansion beyond the existing Latin-script pair; Tamil script and Tamil–English code-switching are separate conditions |
| Simplified Chinese (`zh-Hans`) | Additional writing-system coverage; this text condition does not test spoken Mandarin or Cantonese |
| Spanish (`es`) | Continuity with the earlier handoff study; select and document the actual variety during case review |
| Ukrainian (`uk`) | Subsequent extension after the core languages have reviewed coverage |

Target a reviewed five-language core: English, Brazilian Portuguese, Tamil, Simplified Chinese and Spanish. Ukrainian follows as resources permit. An unreviewed pilot may inform feasibility, but it must retain draft labels and cannot stand in for the reviewed evaluation. This is a coverage choice, not a claim that these languages represent all global buyers or a ranking of expected difficulty.

First keep product facts, prices, currency, buyer country and policy constant while changing language. Brazilian Portuguese does not automatically imply a Brazilian company, BRL pricing or Brazilian rules. Regional business conditions form a separate later experiment. The same applies to English: it is not synonymous with US customer identity.

Use multiple reviewed phrasings for material requirements, negation, conditional approval and clarification. Translation artifacts and one awkward sentence must not stand in for a language effect. Distinguish equivalent-task translation controls from separately authored culturally realistic situations; changing the situation changes the comparison.

## Isolate language from workflow

1. Freeze the product facts, buyer intent, authority and expected outcomes. Use the reviewed language core above, beginning with English, Brazilian Portuguese and Tamil for feasibility. Begin with single-language conversations; switching and within-message code-switching are distinct conditions.
2. Repeat English and each tested non-English condition with the same decoding profiles to measure within-language inconsistency. Demonstrate task competence in independently capable model families before attributing a gap to language.
3. Score output-format compliance separately from semantic correctness. Freeze examples before collection; retain malformed responses and do not silently repair them.
4. Compare the conversation against authored correct structured requirements. If supplying the correct record helps, investigate interpretation and representation; this alone does not prove language caused the original error.
5. Supply correct intermediate inputs to each stage separately alongside end-to-end runs. A wrong proposal caused by a lost requirement is different from inventing a capability despite receiving the correct requirement.
6. Hold product-document and policy language fixed initially. Later cross customer language with document language to distinguish understanding the buyer from retrieving or interpreting supporting evidence.
7. Freeze unseen situation families before collection. Obtain independent linguistic and domain review. Use deterministic source-fact and state checks where possible; human review is needed for nuanced claims and escalation quality.

## Reporting and reusable outputs

Report each model and language separately, with matched English comparisons and within-language repeats. A model that fails the English task cannot support a clean claim that its non-English failures are language-specific.

For every matched case report extracted constraints, unsupported claims, evidence references, escalation, proposal correctness and authorized state changes. Identify the first observable divergence and whether controlled intermediate inputs restore performance. Include stage and end-to-end denominators, English-repeat controls, raw outputs, source revisions and appropriate uncertainty estimates based on independent situations.

Potential reusable artifacts: a reviewed product-claims dataset, a synthetic enterprise-sales environment, adapters for existing agent frameworks, a local regression command, and an intervention evaluated on untouched cases. These are planned deliverables, not an assertion of novelty or adoption.

Before experiments: implement the capability/document store and stateful sales workflow; freeze case families and scoring; obtain language/domain review; then run development and a separate evaluation. Existing static handoff and injected order controls cannot substitute for these sales experiments.


## First executable pilot

The [frozen discovery pilot](../experiments/sales-pilot/PROTOCOL.md) implements 30 AI-authored draft cases in English, Brazilian Portuguese, Tamil, Simplified Chinese and Spanish. It schedules 720 calls across Qwen3-4B and Phi-4-mini, separating requirement extraction, direct product-fit judgment, correct-record judgment and generated-record judgment. This bounded pilot has no outbound proposal, live CRM, specialist interaction or contract execution. See [collection status](../experiments/sales-pilot/EXECUTION_HISTORY.md).
