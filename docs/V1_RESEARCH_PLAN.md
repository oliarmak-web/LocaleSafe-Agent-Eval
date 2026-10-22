# From public prototype to a stronger research contribution

**Recommendation:** publish the current work as an exploratory development release. Build the next study around a narrow, testable safety question. Citation potential depends on independent usefulness and evidence; publication alone does not establish it.

## Proposed question

**Do language-aware evaluations and monitors catch unsafe service-agent actions that English-only checks miss, beyond the model's ordinary inconsistency?**

Focus on permission and correction: the wrong appointment or account, a changed instruction, a rejected proposal, and approval that no longer applies after an edit. Measure both attempted violations and the state changes that actually occur. Include approved actions, so refusing everything cannot earn a good safety score.

## What must improve first

| Current limit | Next requirement |
|---|---|
| AI-authored draft translations | Independent bilingual review of meaning and expected outcome; record disagreements and corrections |
| Six templates with five variants each | More independent situations, with development and held-out sets separated by scenario family |
| Weak English performance | Predeclare an English competence threshold; report models that fail it rather than interpreting a floor as a language gap |
| Two small models from one family | Capable models from different families; document native tool-calling versus prompted JSON interfaces |
| Seeded correction history also supplies a JSON example | Cross example/no-example with correction/no-correction, keeping other information fixed |
| Different outputs may reflect normal randomness | Repeat English against English as well as English against other languages; compare with deterministic decoding |
| Bounded decisions | Real sandbox tool loops with rejection, re-confirmation, stale approval and tool errors |

Independent review is necessary work; an additional model-generated translation is not a substitute. Start with a small reviewed pilot and agree on a compute budget before scaling. Do not assume the full study will fit free GPU quotas.

## Monitoring experiment

Compare English-only checks, an overall multilingual score, and checks separated by language and task. Use the same sampling and alert budgets. Introduce known regressions affecting one language, one tool step, or every language.

Keep the same language-independent permission and action safeguards on all traffic in every condition. “English-only” means the evaluation/canary coverage, not permission to leave other users unprotected. Include these shared safeguards as a baseline. If they catch a failure equally well in every language, report that no extra language-specific monitor was needed for that failure type.

Measure missed unsafe actions, false alarms and detection delay. Calibrate thresholds on development data, then freeze them before the held-out test. This can establish whether extra monitoring adds value, rather than assuming that it does.

Report outcomes by language and task, including successful approved actions, unnecessary refusal, user correction and handoff. Estimate uncertainty over independent scenarios; repeated generations are nested observations. Predeclare primary comparisons and label additional analyses exploratory.

## U.S. relevance and global reuse

Start with appointment changes, customer-service account changes and interpreter requests. The practical question is whether an agent respects the user's intended record, requested language and permission to act. These workflows can support both domestic multilingual services and international products.

Keep language, region, date convention and organizational policy separate. Use a common action contract with reviewed local policy packs. A U.S. scenario translated into another language does not by itself validate a workflow in another country. Healthcare examples cover administration only; clinical safety is outside scope.

## Position against existing work

- [LangDrift](https://github.com/RubenGlez/langdrift) already offers a harness for comparing tool behavior across languages. A multilingual harness alone is not a strong novelty claim.
- [Actions Speak Louder than Words](https://arxiv.org/abs/2608.11110) studies cross-language action-policy retention and controls for within-language inconsistency. Our next study must account for that baseline too.
- [GAIA-v2-LILT](https://arxiv.org/abs/2604.24929) examines how translation and task misalignment can distort evaluation. Translation review is part of measurement validity.
- [MASSIVE-Agents](https://aclanthology.org/2025.findings-emnlp.1099/) and [MAPS](https://aclanthology.org/2026.findings-eacl.42/) already establish multilingual tool/agent evaluation as a research area.

The candidate contribution is a reviewed permission-and-correction suite plus a controlled study of monitoring effectiveness. Its novelty still needs a fuller related-work review and the experiment itself. No claim of being first is made.

## What makes the release useful to cite

Provide a versioned dataset and schema, reviewer/provenance notes, runnable adapters, a frozen protocol, all outputs, a concise technical report and an archived release with a persistent identifier. The repository already has CITATION.cff; a DOI archive and research paper are not yet created. Seek an independent reproduction or an integration into an existing evaluation project, with permission and proper attribution.

Success means another team can use or reproduce a specific result. Citation counts, adoption and production safety improvements remain unproven.
