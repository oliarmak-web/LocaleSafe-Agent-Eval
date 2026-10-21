# Release status — October 21, 2026

## Implemented

- Offline CLI; no model calls, keys, UI hosting, or tool execution.
- Explicit schemas validated in Python and paired scenario-family checks.
- Observable decision/tool scoring, paired gaps, per-case output, artifact hashes.
- 18 synthetic multilingual examples with disclosed draft translation status.
- Positive and deliberately faulty fixtures; evaluator and CLI regression tests.
- MIT license, contribution guide, security guidance, CI, research protocol.
- Genuine CPU-based Qwen3-0.6B pilot: 54 cases × two prompts; exact raw artifacts and local-model collection code.
- Separate format, decision, and tool diagnostics; paired English reference outcomes in both directions.
- Explicit benchmark registry: external benchmarks are not claimed as completed runs.

## Before announcing a research baseline

- Independent translation and domain-policy review.
- Larger reviewed real-model baseline collection; the initial small-model pilot is exploratory only.
- Frozen held-out scenario families, uncertainty analysis, external reproduction.
- Fuller related-work review and an honest baseline technical report.
- Confirm HQ Labs ownership/affiliation wording; no organizational claim is currently made.
- Preserve a sanitized original notebook as a historical artifact after exact-source verification.

## Before public visibility

- Owner review of code, license, attribution, and public description.
- Inspect all tracked files/history for secrets and personal material.
- Enable GitHub private vulnerability reporting and available secret scanning protections.
- Confirm repository visibility explicitly. Local development and a private GitHub push do not make the repository public.

Do not describe synthetic fixture pass rates as model performance, validated safety, research impact, or external adoption.
