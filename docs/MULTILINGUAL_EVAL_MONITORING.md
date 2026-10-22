# Is English testing enough?

**Research question:** when an agent succeeds in English, does the same request succeed in another language? If it fails, is the cause language understanding, the instructions, the conversation history, or the surrounding software?

A second question follows: **what extra testing and monitoring would catch those failures?**

## What our evidence says

For Qwen3-1.7B, English succeeded in 11 of 60 ordinary-request decisions. Among those same 11 English successes, the matched request failed in Spanish four times, Ukrainian six times, Chinese seven times and Haitian Creole nine times. These are overlapping comparisons using the same English controls; do not add them together as independent cases.

That is a concrete signal that passing an English check did not guarantee success on its translated counterpart in this setup. Draft translations, weak overall performance and a small set of templates prevent a broad claim about language as the cause.

English and Spanish each scored 11/60 overall, yet four English successes failed in Spanish and four Spanish successes failed in English. Matching individual requests reveals differences that equal overall scores conceal.

Other failures happened in English too. Supplying the correct facts and translating instructions did not reliably solve them. Correction results also changed across models. Language is one factor to investigate; it is not an adequate explanation for every failure.

## What extra evaluation should add

Use the same standards for correct actions and user permission in every language. Add coverage that an English test cannot provide:

| Addition | What it checks |
|---|---|
| Human-reviewed equivalent requests | Whether changing language changes the outcome |
| Corrections, negation and language switching | Whether the agent preserves intent across conversation turns |
| Language separate from locale and preference | Whether it guesses date conventions or interpreter needs incorrectly |
| Translated instructions and tool-result text | Which part of the language setup introduces a failure |
| Scores for each language, task and model version | Whether an overall average conceals a regression |

First establish that the model can handle the English tasks well. Our low English baseline scores limit how much these runs can explain about language differences in otherwise capable agents.

## What monitoring could add

**Proposed; not implemented or validated in production.** Keep existing action and permission checks, then examine results by request language, task, model and prompt version. Include mixed/unknown language rather than forcing a confident label. Language does not determine a user's region.

Track task completion, wrong records or action details, failed tool calls, unapproved-action attempts, repeated clarification, user corrections and failed interpreter handoffs. Some require reviewed outcomes or user feedback; a successful API response alone cannot establish success.

Compare each language with its own earlier performance and with comparable English tasks. Show traffic counts and uncertainty. Different task mixes or tiny samples can make raw language comparisons misleading. Use redacted event summaries where possible; raw conversations are not required for every metric.

## The next experiment

Compare English-only checks, an overall average, and checks separated by language on the same reviewed test set. Introduce known failures affecting one language or one workflow step. Measure which monitoring approach detects them, how quickly, and how often it raises a false alarm. This would test the added value of language-aware monitoring directly; our current study has not done so.

## Position in the field

We have not audited how most companies stress-test agents. English-first coverage is the motivation to investigate, not an industry-wide finding from this project. Existing work includes [MASSIVE-Agents](https://aclanthology.org/2025.findings-emnlp.1099/) and [MAPS](https://aclanthology.org/2026.findings-eacl.42/); multilingual agent evaluation already exists. LocaleSafe's focus is practical service-workflow diagnosis and testing what English-only checks can miss.
