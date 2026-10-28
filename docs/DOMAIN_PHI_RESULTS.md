# Cross-domain intent feasibility: results

720 greedy microsoft/Phi-4-mini-instruct calls; 180 draft rows, five fictional policies and six languages. Six shared template families, no independent domain/language review, repeats or held-out evaluation.

## English task screens

| Domain | Full history | Reference record | Passed 5/6 in both? |
|---|---:|---:|---|
| security | 5/6 | 3/6 | False |
| finance | 3/6 | 4/6 | False |
| health_admin | 3/6 | 4/6 | False |
| insurance | 4/6 | 4/6 | False |
| telecom | 4/6 | 5/6 | False |

A failed English screen limits language attribution. Even a pass does not establish broad domain competence.

## Separate extraction and action checks

| Domain | Language | Intent extraction | Full-history action | Reference-record action | Generated-record action | Rejected execute attempts, history/generated |
|---|---|---:|---:|---:|---:|---:|
| security | en | 2/6 | 5/6 | 3/6 | 3/6 | 0/0 |
| security | es | 2/6 | 5/6 | 3/6 | 4/6 | 0/0 |
| security | hi | 2/6 | 4/6 | 3/6 | 2/6 | 0/0 |
| security | pt-BR | 2/6 | 5/6 | 3/6 | 4/6 | 0/0 |
| security | zh-Hans | 1/6 | 4/6 | 3/6 | 3/6 | 0/0 |
| security | ta | 0/6 | 3/6 | 3/6 | 1/6 | 0/0 |
| finance | en | 0/6 | 3/6 | 4/6 | 3/6 | 0/1 |
| finance | es | 1/6 | 3/6 | 4/6 | 4/6 | 0/1 |
| finance | hi | 2/6 | 4/6 | 4/6 | 3/6 | 0/2 |
| finance | pt-BR | 1/6 | 3/6 | 4/6 | 3/6 | 0/1 |
| finance | zh-Hans | 1/6 | 3/6 | 4/6 | 3/6 | 0/2 |
| finance | ta | 0/6 | 5/6 | 4/6 | 3/6 | 0/1 |
| health_admin | en | 1/6 | 3/6 | 4/6 | 3/6 | 1/0 |
| health_admin | es | 1/6 | 3/6 | 4/6 | 3/6 | 0/0 |
| health_admin | hi | 0/6 | 3/6 | 4/6 | 2/6 | 0/0 |
| health_admin | pt-BR | 0/6 | 3/6 | 4/6 | 2/6 | 0/0 |
| health_admin | zh-Hans | 0/6 | 2/6 | 4/6 | 1/6 | 0/0 |
| health_admin | ta | 0/6 | 4/6 | 4/6 | 1/6 | 0/0 |
| insurance | en | 0/6 | 4/6 | 4/6 | 5/6 | 0/0 |
| insurance | es | 0/6 | 4/6 | 4/6 | 3/6 | 0/2 |
| insurance | hi | 0/6 | 4/6 | 4/6 | 2/6 | 0/0 |
| insurance | pt-BR | 0/6 | 4/6 | 4/6 | 4/6 | 0/1 |
| insurance | zh-Hans | 0/6 | 3/6 | 4/6 | 2/6 | 0/1 |
| insurance | ta | 0/6 | 3/6 | 4/6 | 3/6 | 0/1 |
| telecom | en | 1/6 | 4/6 | 5/6 | 3/6 | 0/0 |
| telecom | es | 1/6 | 3/6 | 5/6 | 3/6 | 0/0 |
| telecom | hi | 0/6 | 1/6 | 5/6 | 2/6 | 0/0 |
| telecom | pt-BR | 0/6 | 4/6 | 5/6 | 2/6 | 0/0 |
| telecom | zh-Hans | 2/6 | 2/6 | 5/6 | 4/6 | 0/0 |
| telecom | ta | 0/6 | 2/6 | 5/6 | 1/6 | 0/0 |

Rejected-attempt entries are counts from six calls per evidence condition. All actions remain inside the local guard; they are not customer outcomes. Clarify/escalate means selecting a checkpoint disposition, not completing a conversation or transfer.

## Limits

Customer language changes while policies, currency and declared locale remain fixed. These are text-only, single-language histories; no ASR, dictation product, cultural group, language switch, deployed service or legal/clinical decision was evaluated. Raw outputs, failed attempts and field scores remain available. More calls on these shared templates do not add independent workflows.
