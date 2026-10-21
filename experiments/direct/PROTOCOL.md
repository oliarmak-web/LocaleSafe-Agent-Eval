# Direct answers across five languages

Frozen development protocol, not a preregistered or held-out study.

- English, Spanish, Simplified Chinese, Ukrainian, Haitian Creole; draft translations.
- Per language: two numeric-date families × US/GB/unspecified locale, one ISO-date control, one localized month-name control. 40 items; two sampled generations each.
- Fixed Qwen3-0.6B, English policy, decoding, explicit locale, and parser. User language varies; policy language does not.
- No offered answers or letter labels. Return an ISO date or CLARIFY. Primary parsing accepts only that scalar; a declared secondary parser removes only an enclosing Markdown fence.
- Score parsing, date interpretation, clarification, and sandbox outcome separately. Replay decisions through the same fixed adapter, which handles confirmation correctly by construction.

The sandbox user always approves. Wrong committed dates measure potential downstream error under that assumption, not real-world harm. Adapter success does not demonstrate autonomous planning. ISO/month-name controls test whether numeric-convention ambiguity drives failures. Compare with the previous letter-choice experiment only on overlapping numeric English/Spanish tasks; methods and repetitions differ, so this is a cross-check, not a paired causal estimate.

Retain exact prompts, raw answers, seeds, hashes, versions, and every failed output. Two repeats are nested within items; eight variants per language are not eight independent domain families. No language ranking, significance, equivalence, culture-wide competence, or clinical claim. Next: human review, stronger models, new held-out families, interactive tool calls.

Post-collection amendment: the archived run used an inconsistent scripted reply in GB cases. Original cases and scores are preserved. A declared post-hoc replay corrects only that reply to the intended date. Current development cases include this fix; the archived protocol predates the amendment.
