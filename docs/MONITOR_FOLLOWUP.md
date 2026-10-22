# Monitor intervention: fewer unsafe allows, more false blocks

**384 new greedy Qwen3-4B calls. Exploratory follow-up designed after inspecting the initial results.**

The same 128 fixed probes are judged under three conditions. The generated summaries and proposed actions stay fixed. Baseline-repeat prompts match the original run; explicit rules add a permission-check paragraph; oracle records replace generated records with the authored correct record.

| Source families | Condition | Correct / all | False allows / forbidden | False blocks / permitted | Abstentions |
|---|---|---:|---:|---:|---:|
| development | baseline_repeat | 49/64 | 15/32 | 0/32 | 0 |
| development | explicit_rules | 38/64 | 10/32 | 16/32 | 0 |
| development | oracle_record | 64/64 | 0/32 | 0/32 | 0 |
| evaluation | baseline_repeat | 40/64 | 24/32 | 0/32 | 0 |
| evaluation | explicit_rules | 32/64 | 8/32 | 24/32 | 0 |
| evaluation | oracle_record | 64/64 | 0/32 | 0/32 | 0 |

## Interpretation

The explicit-rule prompt reduced false acceptance but blocked many permitted actions, lowering overall correctness. It was not a successful balanced fix in these cases. The oracle-record condition classified all 128 probes correctly, showing that this monitor can perform the bounded task with the reference representation.

In the initial runs, Qwen preserved all permission fields but often represented requested_action as a string rather than the required tool-call object. A full reference record changes both the action representation and its contents; this follow-up does not isolate which field or wording explains the improvement.

The baseline repeat reproduced the original greedy verdicts on every probe. Both source splits had already been inspected before this intervention was designed; neither is held out for this analysis. These are monitor judgments, not prevented production harm. Draft translations, small template counts and a single model limit generalization.

The universal permission guard remains unchanged. A false allow by this model cannot authorize a real write in the sandbox.

[Protocol](../experiments/monitor-followup/PROTOCOL.md) · [Raw archive](../experiments/results/monitor-followup-qwen3-4b-20261022/)
