# Why this work is credible and useful

**LocaleSafe is an auditable development study and a reusable testing tool.** Its strongest contribution is helping teams investigate why an agent chose the wrong action.

## Why the evidence is credible

- **Comparable requests:** the same authored situation appears in five languages, with the same service data and expected action. Draft translations still require independent review.
- **Specific controls:** we change the instruction language, supply the correct facts directly, and test a correction after an earlier wrong proposal.
- **Action checks:** a simulated service checks appointment IDs, available times, requested interpreter language and permission boundaries. A fluent answer or well-formed command alone cannot pass.
- **Inspectable evidence:** all 1,800 recorded outputs, prompts, settings, failures and source snapshots are archived. Both retrieved raw files match their original Colab hashes. Scores can be recomputed without running a model.
- **Visible limitations:** interrupted runs and a lost temporary archive are documented. Repeated examples are not presented as independent real-world situations.

The supported claim is narrow: these models, with these instructions and tasks, produced these recorded outcomes. Automated tests check the software and saved evidence; they do not establish translation quality or real-world reliability.

## Why engineering teams should care

Our larger model produced 278 correctly formatted commands out of 300, but only 37 correct actions. This demonstrates a concrete testing gap: checking that a command can be read is insufficient to check that it does what the user requested.

Potential applications:

| Product workflow | What a team could test |
|---|---|
| Appointment or customer-service assistant | Changes the requested record and time, including after a correction |
| Booking or account assistant | Respects “check only” and “do not submit” |
| Interpreter handoff | Uses the requested language without guessing the user's region |
| Model or prompt upgrade | Preserves working behavior across the languages the product supports |

The intended benefit is a clearer engineering decision: investigate translation, command formatting, action details, conversation history or the surrounding workflow. We have not measured production incident reduction, cost savings or customer impact.

## Where it fits in research

Multilingual tool use is an established research area. [MASSIVE-Agents](https://aclanthology.org/2025.findings-emnlp.1099/) evaluates 52 languages and also studies example prompts and translated instructions. [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) evaluates accurate tool calling and multi-turn interactions. We have not run either benchmark, and our scores are not comparable to theirs.

LocaleSafe adds authored service cases, executable checks and transparent diagnostic experiments. Its contribution is the implementation and evidence, rather than a claim to invent multilingual evaluation.

## What would make the research stronger

Independent translation review; new tasks kept separate from development; positive approval cases; full user–agent conversations; models from other families; external reproduction. Until then, it is a useful foundation for research and engineering tests, with limited evidence for wider conclusions.

[Concrete next-study plan and related-work overlaps](V1_RESEARCH_PLAN.md).
