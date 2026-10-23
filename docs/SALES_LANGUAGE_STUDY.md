# Sales-agent language diagnostic

**Proposed pilot; no sales-model results collected.** October 23, 2026. The working use case is a simulated quote-to-order flow, pending selection of the sales workflow. This requires a new catalog, state model, reviewed cases and collector; existing appointment or order-control results do not establish sales performance.

## Question

Does changing the customer's language change successful completion of the same valid sales request? If so, is the first observable failure in understanding requirements, applying catalog/policy facts, preparing a quote, preserving corrections or executing the approved action?

Do not treat more orders as universally better. A request for a quote is not permission to place an order. Correct refusal, waiting and clarification can be successful outcomes. No simulated completion metric establishes real conversion, customer abandonment or lost revenue.

## Concrete workflow

Use a fixed fictional product catalog, inventory, prices, shipping charges and discount rules. Start with physical accessories rather than regulated products. Keep SKU identifiers, amounts, currency, inventory and rules identical across languages.

Example request: “Two USB-C chargers. Maximum total USD 60 including delivery. Show me the quote; do not order yet.” The user then corrects quantity or shipping preference, or explicitly approves the exact final quote. The sandbox records the selected items, quoted total, approval and resulting order. No real purchase occurs.

| Stage | Check | Example failure |
|---|---|---|
| Requirements | Product attributes, quantity, total budget, shipping preference, approval scope | Understands two chargers as two cables or treats a total budget as a per-item budget |
| Catalog and rules | Grounded SKU, inventory, permitted discount, supported delivery | Invents stock or a discount; chooses a product that fails the stated requirements |
| Quote | Exact SKU/quantity, item subtotal, shipping and final total | Omits shipping and recommends an order above the budget |
| Correction/handoff | Latest quantity, budget, delivery and approval replace the earlier values | Summary preserves the old quantity after the customer changes it |
| Order | Exact approved quote, one resulting effect | Commits a quote-only request, submits a superseded quote or creates duplicate orders |

The same action can be permitted but fail the sales task: an approved product may violate the user's previously stated requirements. Score authorization and task completion independently.

## Controls needed before language attribution

1. Match each situation across English and independently reviewed Tamil; retain Spanish as an existing project comparison if review is available. Start with same-language conversations. Add switches and code-switching as separate later conditions.
2. Repeat English prompts with the same decoding profiles to measure ordinary inconsistency. Use multiple capable model families and demonstrate English task competence before interpreting a language gap. An English screen does not prove equivalence of translated cases.
3. Score JSON contract compliance separately from valid-action semantics. Freeze output examples before collection; do not repeat the earlier formatting confound or silently repair responses.
4. Compare the full conversation against an authored correct requirements record. Improvement with that record is a lead about input interpretation/representation, not proof that translation alone caused the error.
5. Feed authored correct inputs to each downstream stage separately, alongside end-to-end runs. This distinguishes a bad quote caused by wrong extracted quantity from a pricing failure despite the correct quantity. It also helps locate recovery after an earlier error.
6. Hold catalog/rule language fixed for the first language comparison. A later crossed experiment can vary customer language and catalog/policy language independently. Currency, regional policy and cultural communication preferences are separate variables.
7. Preserve all attempts, raw prompts/outputs and state changes. Score successful orders, justified waiting/refusal, unnecessary blocks, invalid commands and duplicate effects. Freeze new situation families for later evaluation before looking at their outputs.

## Reporting

For each matched situation, show the English and Tamil outcomes, English repeat consistency, the first observable divergence and whether supplying correct intermediate facts restores the result. Report the denominator at each stage and in the end-to-end run; conditional stage scores can hide failures that prevent reaching that stage. Use uncertainty estimates based on independent situations rather than treating repeated generations as independent samples.

Do not write “Tamil causes sales loss” from synthetic failures. A defensible result is: “On these reviewed requests, a larger share of failures appeared during requirement extraction in Tamil; the gap shrank with correct structured requirements and exceeded the observed English-repeat difference.” That sentence is an example of the claim structure, not an observed result.

## What must be built next

Freeze the selected sales workflow and policies; implement the catalog and quote/order sandbox; author and independently review paired requests; add model adapters and stage scorers; run development and then a separately frozen evaluation. Tamil fluency review and sufficiently capable model coverage are outstanding dependencies. Earlier static handoff results and injected SQLite controls remain separate evidence.
