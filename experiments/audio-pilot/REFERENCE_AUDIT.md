# Post-collection reference audit

October 27, 2026. The original protocol, selected clips, released reference strings and all model outputs remain unchanged.

The [MINDS-14 source paper, section 4](https://arxiv.org/html/2104.08524) describes generating written transcriptions with Google ASR. Those released hypotheses must not be treated as independently verified human-gold transcripts for evaluating another recognizer.

Our MINDS character-edit ratios therefore measure disagreement with the released text, not validated recognition error. Extra words in a Whisper response cannot be called hallucinations merely because the supplied reference is shorter; omissions or errors in either transcription remain possible without audio/reference review. No clips or unfavorable scores were removed after this discovery.

FLEURS is a read-speech corpus with released reference text. LocaleSafe has not independently reviewed its selected audio/text alignment either. The sample has only two clips per configuration, and contents differ across languages. Neither corpus supports cultural conclusions, a stable language ranking or downstream action-safety claims from this smoke test.

The paired automatic/supplied-language comparison remains a within-clip output comparison, independently of whether the source reference is complete. Reports now identify reference provenance and exact paired-output agreement. This is a post-hoc interpretation/provenance clarification, not a new scoring rule or repaired generation.
