# Saved approval, resumed orders and duplicate effects

October 22, 2026. Provider-free engineering controls, authored and implemented with AI assistance. **No models, translated prompts or external services are involved.** This is not a new multilingual benchmark result or a claim that the mechanisms are novel.

## What runs

A SQLite database holds two fictional orders, a versioned current approval, saved plans and an effect log. Each test saves a plan, optionally changes or withdraws approval, closes the database connection, reopens it and resumes the plan. The retry schedule closes and reopens again before submitting the same operation ID.

Three execution policies run on the same seven schedules. The approval-aware policies compare the saved action and approval version against current approval in the same transaction as the write. The final policy also recognizes previously executed operation IDs and rejects conflicting payloads.

The simulator changes an order's cancellation status or delivery address. It models local effects, not real dispatch, refunds, shipping eligibility or distributed execution. Closing a connection is not a process crash. Concurrency, real authentication and multi-tenant access are untested.

## Results

| Policy | Correctly completed schedules | Unapproved effects | Duplicate effects |
|---|---:|---:|---:|
| Trust saved checkpoint | 2/7 | 4 | 1 |
| Recheck current exact approval | 4/7 | 0 | 1 |
| Recheck and deduplicate operation IDs | 5/7 | 0 | 0 |

The seven schedules are unchanged approval, withdrawn approval, permission moved to another order, changed delivery address, proposal-only withdrawal, a retry, and a refreshed valid plan. Proposal-only and withdrawal are equivalent at the executor boundary: no write is approved. Natural-language interpretation of their difference is outside this experiment.

**Three distinct checks are needed.** Current approval prevents stale writes. Deduplication prevents repeated dispatch. A new plan is still needed when the customer changes the requested order or address. In both replacement schedules, the final policy blocks the obsolete plan but leaves the new request incomplete. Reporting only zero unauthorized writes would hide that failure.

These results are expected consequences of authored schedules and policy implementations. They do not establish real-agent failure prevalence, framework vulnerabilities, statistical significance or research priority over earlier authorization and workflow literature. The experiment makes a reproducible executor baseline for a later model study.

## Run and inspect

Python 3.11+, no extra packages, keys or GPU:

```sh
python -m experiments.run_order_controls --output-dir reports/order-controls-local
```

Choose an unused output directory. Inspect `results.json` for statuses, the latest approved action, expected and final order fields, effect counts and database hashes. SQLite files and source snapshots are retained locally. The tracked [result artifact](../experiments/analysis/order-controls/results.json) includes all state/effect outputs and source hashes; database binaries remain local artifacts. [Protocol](../experiments/order-controls/PROTOCOL.md).

## Next model study

Add reviewed user conversations and independently authored situation families; ask models to resume or revise saved plans against the same state checks. Hold workflow and permission transitions fixed across languages. Score invalid commands, stale attempts, duplicate effects and completion of the corrected request separately. Tamil remains a priority for reviewed language expansion. The queued Mistral/Phi format intervention first checks whether prompt-example presentation is a confound in the existing command contract; no new GPU outputs have been collected for it.
