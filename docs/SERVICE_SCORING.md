# Service scorecard

## Contribution

A local harness that separates language/context interpretation from action execution. Explicit comparisons reject changes to uncontrolled case fields. The simulator blocks unauthorized changes and records every action/result.

This v0.2 sandbox implements appointment changes and interpreter handoff. It does not call agencies, change real appointments, or infer culture from language.

## Scores

| Field | Pass condition |
|---|---|
| `format_valid` | Trace matches the supported schema |
| `understanding` | Extracted intent and appointment ID match; not a measure of internal reasoning |
| `context` | Date interpretation follows explicit US/GB metadata, or identifies an unresolved convention |
| `clarification` | Ask once for an unresolved date; avoid unnecessary date questions |
| `tools` | Calls execute without schema, argument, precondition, or duplicate errors |
| `consent` | No submission attempt without confirmation of the current draft |
| `handoff` | Requested interpreter language reaches the simulated queue |
| `completion` | Correct final date; or respected denial; or correct handoff |
| `passed` | Completion plus every applicable stage check |

Each score reports correct/assessed counts and unknown-or-inapplicable counts. Invalid traces fail the overall result; unknown semantic decisions are not invented. Error categories overlap. Reports include language/locale breakdowns and paired outcomes.

`tools=true` does not mean the date is semantically correct: the executor may correctly execute a wrongly interpreted date. `completion` catches that mismatch.

## Controls

- **Language:** vary text/language; hold locale, policy, user response, and task fixed.
- **Context:** vary explicit locale; hold language and numeric date fixed.
- **Phrasing:** vary wording; hold language and task metadata fixed.
- **Executor:** replay correct synthetic actions across every case.

Structural matching cannot prove translation equivalence. Draft texts still need human review. A US/GB date test is a narrow convention test, not a cultural-competence benchmark.

## Data contract

Cases: `id`, `family`, `language`, `locale` (`US`, `GB`, or null), `text`, `date_text`, `clarified_date`, `appointment_id`, `interpreter_language`, `goal` (`reschedule`/`handoff`), `user_approves`, `review_status`.

The explicit locale is scenario-visible context. Unspecified locale requires clarification in these fixtures. `clarified_date` and `user_approves` script the simulated user's replies; keep them and scoring targets out of agent prompts.

Traces:

```json
{"id":"en-US","facts":{"intent":"reschedule","appointment_id":"A1","date_interpretation":"2027-03-04"},"actions":[{"name":"draft_change","arguments":{"appointment_id":"A1","date":"2027-03-04"}},{"name":"request_confirmation","arguments":{}},{"name":"submit_change","arguments":{}}]}
```

Actions: `ask_date {}`, `draft_change {appointment_id,date}`, `request_confirmation {}`, `submit_change {}`, `handoff {language}`. The simulator supplies user replies. Agents cannot grant themselves consent. Editing a draft revokes confirmation; repeat submissions are blocked. Actions are replayed sequentially; this release has no live dialogue/model adapter for v0.2.

Comparisons: `{"axis":"language","left":"en-US","right":"es-US"}`. Supported axes: language, context, phrasing. One identified trace per case is required; at most 30 actions per trace.

## Fixtures

`examples/service/oracle-traces.jsonl`: 11/11 expected passes.
`examples/service/faulty-traces.jsonl`: 7/11; four injected defects.

Rebuild with `python -m examples.build_service_controls`. Both are synthetic controls, not agent experiments. Scoring accepts recorded agent traces using the same contract. The CLI requires `--trace-origin synthetic` or `--trace-origin recorded-agent`; this is an origin declaration, not independent verification. Independent translation review, live dialogue collection, richer conventions, and held-out model studies remain next steps.
