# What we learned, in plain English

We recorded **1,800 decisions from two models in five languages**. The tasks asked a model to check availability, respect a correction, choose a suitable time, handle an unavailable time, request an interpreter, or follow a language switch.

The central question is whether passing English tests is enough. In this setup, some requests passed in English and failed in another language. That supports checking each supported language; it does not prove that language alone caused the failure. [What extra evaluation and monitoring should test](MULTILINGUAL_EVAL_MONITORING.md).

## 1. Looking correct is different from being correct

The larger model returned 278/300 commands in the required format. Only 37/300 selected the right action and details. In 239 cases, it used the right command type with wrong details, such as an appointment ID or time.

**Why it matters:** a format check can pass while the system is preparing the wrong change. Teams need to check the resulting action and record, too.

## 2. Language differences changed with the setup

When correcting an earlier wrong proposal, the small model succeeded in 58/60 English cases and 2/60 Haitian Creole cases. The larger model scored 10/60 and 16/60 respectively. Ukrainian scores were 39/60 and 38/60.

**What this means:** language is worth testing in the exact model and conversation setup a team uses. These results do not establish that one language is generally harder or less reliable. The translations still need independent review.

## 3. Translating instructions did not reliably help

For the larger model, translated instructions fixed six cases but broke eleven cases that had previously worked. Giving it the correct facts directly produced 6/60 correct commands, compared with 11/60 for ordinary English requests.

**What this means:** translation and fact extraction are not guaranteed fixes. The model may still struggle to turn information into the correct command.

## 4. Earlier conversation can change the result

The small model failed every ordinary request under the exact-format scoring rule, but corrected 187/300 earlier proposals. The correction test also showed it a JSON command example.

**What this means:** the conversation history may affect both formatting and decisions. This experiment cannot separate the benefit of an example from the ability to understand a correction.

## 5. The test system itself can cause errors

An earlier date experiment contained an inconsistent scripted user reply. Fixing that reply reduced wrong simulated changes from 13 to 1, using exactly the same model answers.

**What this means:** audit the test environment before blaming the model or language.

## What we can claim

LocaleSafe can expose different kinds of failure and check whether a proposed fix helps these recorded tasks. The evidence supports further testing; it does not prove broad language bias, cultural competence, or real-world safety.

We need reviewed translations, more varied tasks, stronger models from other families, and full conversations before making wider claims.

[Methods, tables and raw evidence](WORKFLOW_STUDY.md) · [Why this is credible and useful](WHY_IT_MATTERS.md)

Earlier experiments: [date interpretation](../experiments/results/direct-five-language-20261021/INSIGHTS.md), [answer-choice bias](../experiments/results/attribution-20261021/INSIGHTS.md), [initial multilingual pilot](../experiments/results/qwen3-06b-20261021/RESULTS.md).
