# Use-case priorities: October 2026–April 2027

**Next model-study priorities.** A local injected-plan order-control prototype is now executable; model-driven and multilingual order coverage remains proposed. Priorities reflect fit with LocaleSafe and observed technical work, not measured market demand or a claim of unique research territory.

## Focus

Test whether an agent follows the user's latest approval when a customer-service request is corrected, paused, summarized or delegated. Compare languages while holding the action and workflow fixed. Measure both unauthorized attempts and valid requests unnecessarily blocked.

[NIST's agent standards initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative) identifies identity, authorization and interoperability as active work. [LangGraph's interrupt documentation](https://docs.langchain.com/oss/python/langgraph/interrupts) describes persisted approval pauses and resumed execution. These support the relevance of approval state across workflow boundaries; they do not establish how often deployed agents mishandle it. Continued demand over the next six months is a forecast.

## Priorities

| Priority | Use case | Concrete scenario | Useful result |
|---|---|---|---|
| 1 | Customer-service order changes | A customer approves cancelling order A, then withdraws approval or asks to change order B instead | Which record changed, whether the latest exact action was approved, whether the legitimate request completed |
| 2 | Approval after a pause or handoff | An agent saves an approved action; the user changes the item, date or scope before the run resumes | Whether stale approval is reused; whether revalidation prevents it without excessive refusal |
| 3 | Draft versus send | A user requests a draft reply, later approves one recipient or revises the draft before sending | Whether exact content and recipient remain within approval; whether retries cause duplicate sends |
| Later | Purchase approval | A user changes the merchant, item or price limit before checkout | Whether the final proposed transaction still matches current permission |

Use synthetic stores and a local effect log. The [order controls](ORDER_CONTROLS.md) implement local cancellation/address changes, database reopen and sequential retries with injected plans. Model-driven changes, process-crash recovery, message content, recipient scope and payment constraints still require additional environments. Existing mock appointment/delivery/notification labels do not establish that coverage.

Payments have a concrete standards signal in [Google's AP2 work](https://blog.google/products-and-platforms/platforms/google-pay/agent-payments-protocol-fido-alliance/), but add protocol complexity and strong existing security research. Keep them a later sandbox extension.

## Avoid duplicating a general customer-service benchmark

[Sierra's current τ-bench repository](https://github.com/sierra-research/tau2-bench/blob/main/README.md) documents multilingual customer-service evaluation, including text and voice. General multilingual task completion is already covered. LocaleSafe should investigate a bounded failure mechanism and reproducible controls, not claim to introduce multilingual service-agent evaluation.

Authorization, handoff and monitoring research also overlap this direction. See [the method comparison](HANDOFF_METHOD_COMPARISON.md). The candidate contribution is the reviewed dataset, crossed experiments, component diagnostics and measured interventions. Its novelty still needs comparison against those methods; a new application label is insufficient.

## Next experiment

Start with order changes. Freeze policies and unseen situation families before collection. Vary one factor at a time:

- **Language:** English and Spanish continuity, with Brazilian Portuguese and Tamil prioritized; Simplified Chinese joins the reviewed core and Ukrainian follows. Separate single-language, language-switch and within-message code-switch conditions.
- **Evidence:** full conversation, generated summary and reference record.
- **Workflow:** uninterrupted, paused/resumed, delegated and retried execution. Add these as explicit implementations rather than relabeling static prompts.
- **Enforcement:** model judgment versus a deterministic check against current approval. Report attempted actions separately from executed effects.

First test structured-output compatibility separately from semantic correctness. Keep raw strict scores; any constrained-generation or format-repair arm must be separately specified and reported. The Mistral/Phi development failures show why this control matters.

Report correct completion, invalid commands, unauthorized attempts, realized unauthorized changes, false blocks and duplicate effects. Use paired situations, multiple independently capable model families and uncertainty estimates suited to independent scenario counts. Repeated generations are not additional independent situations. Independent reviewers should verify translated permission and expected state transitions.

## Reusable open-source deliverables

Provide a local order-change sandbox, reviewed and versioned cases, a minimal adapter for one agent framework, a one-command regression check and raw reproducible results. The developer's call to action is: **run your agent against changed approvals before deploying record-changing tools.**

Demonstrate a fix on untouched cases, report its cost in valid task completion, and include a citation file for a stable release. These make the work easier to reuse and cite; citations and adoption cannot be guaranteed.
