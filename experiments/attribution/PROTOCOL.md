# Language or workflow? Controlled probe

Exploratory development experiment. Frozen before collection; not a preregistered study.

## Design

- Interpretation: two ambiguous numeric-date families × three explicit locale conditions × two phrasings × English/Spanish = 24 items.
- Workflow: six English-only tasks with known facts; choose among three action plans. Consent, denial, stale approval, duplication, handoff, clarification.
- Six balanced A/B/C answer orders. Three seeded categorical draws per order. 180 model forwards; 540 sampled choices. Repeated draws reuse fixed model probabilities; they are not independent tasks or full generations.
- Fixed Qwen3-0.6B weights, policy, temperature, parser, and CPU runtime. No API fees or new model downloads.

## Isolation

The model chooses one A/B/C token from masked next-token probabilities. JSON formatting cannot fail. All options appear equally often in each label position. This is recognition among offered answers, not free-form reasoning or native tool calling.

A fixed adapter converts date choices into simulator actions; user replies and consent come from the script. Canonical correct choices must pass all controls. Adapter success does not prove the model can independently plan a workflow. The separate workflow probe tests plan recognition with the language interpretation removed.

Match language and phrasing contrasts by family, locale, answer order, and draw. Shared seeds couple draws; report counts and expected probabilities, not inflated significance. Separate model decision errors, simulator failures, position sensitivity, and English paraphrase sensitivity.

## Limits

Draft translations; two date families; six workflow controls; one small model. No culture-wide competence, population-level language effect, or equivalence claim. Human semantic review, new held-out families, more models, and interactive generation are required next.

No gold answer, scripted clarification reply, or hidden consent response enters interpretation prompts. Workflow prompts explicitly disclose the facts needed for the control.
