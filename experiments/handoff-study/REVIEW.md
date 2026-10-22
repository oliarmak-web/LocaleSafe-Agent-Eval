# Independent bilingual review

Status: not completed. All wording and reference actions remain AI-assisted development drafts.

Review should be performed by English/Spanish speakers independently of the draft generation. Record the reviewer role, date, case/version, disagreements and changes; publish identifying details only with consent.

## First pass: blinded interpretation

Review the event text and visible state without consulting the authored permission/reference-action fields. For each case, record:

1. The latest requested action: wait, propose or commit, including record and value.
2. Whether a write is approved, and its exact scope.
3. Which event changes permission and whether earlier approval remains active.
4. Ambiguities, unnatural phrasing or differences in meaning across language patterns.

Compare the en-en, es-es, en-es and es-en versions within the same situation. Identifier changes are not independent situations. Assess the intended meaning, not whether a particular model happened to answer correctly.

## Second pass: reference adjudication

Compare independent interpretations with the authored references. Resolve disagreement before marking a case reviewed. Preserve the original version and record corrections. Changes after model collection require a new dataset version and an explicitly labeled rescore or new collection; never silently replace archived cases.

Semantic review of generated narrative handoffs is a separate task. In particular, distinguish omitted permission, incorrect approval, wrong record/value, and harmless paraphrase. Automated exact-record fidelity does not evaluate free-text meaning.

The current experiment does not claim completion of this process. A generated translation or another model's agreement is not independent human review.
