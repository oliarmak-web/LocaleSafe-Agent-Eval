# Research protocol

**Question:** When service outcomes differ, is the cause language, context, output handling, or the shared workflow?

## Existing evidence

- v0.1: 108 local Qwen3-0.6B generations; six families × nine language configurations × two prompts.
- v0.2: executable service sandbox and synthetic controls. No v0.2 model study yet.
- All non-English text remains draft. Neither suite is a validated benchmark.

## Next study

1. Review task policies and translation equivalence with qualified reviewers; record disagreements.
2. Add English paraphrases, contextual variants, and separate held-out families. Keep every variant of a family in one split.
3. Freeze models, prompts, tools, output handling, user scripts, retries, and primary metrics.
4. Cross language with explicit locale. Test canonical executor actions before model runs.
5. Repeat generations. Choose sample size from a pilot-based precision/power rationale.
6. Report every failure, stage-specific denominators, paired differences in both directions, and family-level uncertainty.

Shared failure suggests a general task weakness to investigate. English-pass/other-fail is language-associated evidence, not proof of causation. Missing differences in a small sample do not establish equivalence.

Keep post-hoc analysis labeled. Never silently repair selected languages' outputs. Compare constrained output and native tool calling as separate configurations.

## Release gates

Reviewed data → validated simulator → frozen held-out study → reproducible results → independent reproduction.

Future: richer conventions, corrections, code switching, tool outages, and audio. Speech requires separate licensed/consented recordings, reference transcripts, and ASR analysis.
