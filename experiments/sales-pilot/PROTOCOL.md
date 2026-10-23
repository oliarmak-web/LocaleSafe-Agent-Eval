# Enterprise-sales discovery pilot

Frozen before collection, October 23, 2026. **Unreviewed feasibility pilot, not a validated multilingual benchmark.** No real buyers, revenue, product capabilities, legal compliance determinations or purchasing decisions are involved.

## Task and cases

An internal sales assistant assesses a fictional cybersecurity product against mandatory buyer requirements. The catalog supports US data storage and EntraID, up to 3000 employees, a fixed USD 80000 annual price and a minimum 45-day deployment. Case requests specify employees, storage region, integration, budget and deployment deadline. Do not send a proposal or make a commercial commitment.

Six authored situation families: all supported; unsupported storage region; unsupported integration; insufficient budget; impossible deadline; and correction from EU-only to US-only storage. Five matched versions per family: English, Brazilian Portuguese, Tamil, Simplified Chinese and Spanish. All 30 cases and translations are AI-authored drafts with zero independent language/domain reviews. Spanish variety is not yet specified. Tamil script is used; spoken language, code-switching and cultural communication styles are untested. Six translated templates do not represent six independent cases per language or global buyers.

The expected requirements are authored metadata. Product facts, amounts, policy, document language (English) and scenario meaning remain fixed. Customer country and currency do not vary with language. Do not equate Brazilian Portuguese with Brazilian regulations or deployment geography.

## Crossed stages

For each case under greedy, sample-1 and sample-2:

1. Extract the latest five requirements from the buyer conversation.
2. Assess fit directly from the full conversation and product facts.
3. Assess fit using the authored correct requirements and product facts (oracle).
4. Assess fit using the same model's generated extraction and product facts.

Correctly extracted records produce identical oracle/generated assessment messages; condition IDs and reference fit decisions never enter ordinary prompts. Extraction has no catalog access. Generated records are forwarded unchanged if valid JSON objects; malformed replies are preserved as text, not silently repaired. Cases and expected labels remain separate from visible history.

30 cases × 3 profiles × 4 calls = 360 calls per model. Run pinned Qwen3-4B and Phi-4-mini-instruct, 720 retained calls if both complete. These model families do not establish broad language competence; in particular this pilot does not assume equivalent Tamil training or support. Report each model/language separately. English and non-English sampled repeats measure local generation variability; two sampled repetitions are limited, not a full estimate of uncertainty. Greedy is reported separately.

## Collection

Free Colab T4 only, float16 without quantization, batch 8, Transformers 4.57.6, thinking disabled. Extraction cap 128 new tokens; fit assessment cap 96. Native chat templates and pinned revisions/weight hashes from the existing collector registry. Sampling: temperature .7, top-k 20, top-p .8, independent per-row seeded CUDA generators. Seeds match by family/profile/stage across languages and oracle/generated fit conditions; this does not make token sampling equivalent across different prompts. Deterministic stage-wise shuffled schedule seed 20261023; collect all extractions before dependent assessments. Preserve raw outputs, token caps, prompts, dependencies, settings, source snapshots and hashes. No paid APIs or frontend keys.

## Outcomes and interpretation

Strict schema validity and exact requirement/field fidelity are separate. Fit requires both the correct decision and all unsupported fields. Also report decision accuracy, unsupported fit claims, unnecessary escalation and invalid outputs. An invalid record's zero field scores do not prove every underlying fact was misunderstood. Fit claims are internal model judgments, not sent sales promises or realized harm. No CRM, live handoff or outbound message is executed.

Compare matched history accuracy by language against English and within-language sampled variability. Use oracle contrasts to locate a representation/interpretation lead, and generated-record contrasts to investigate propagation. Because structured oracle inputs are language-independent, they are controls, not multilingual ability tests. A downstream error need not have the same cause as extraction error. Do not infer causality from one translated prompt or pool profiles/languages as independent situations.

No model gate, significance test or confirmatory inference is planned for this feasibility run. A low English score, format floor, oracle failures or inconsistent repeats limits language attribution. All six families are development material; there is no held-out evaluation, adoption evidence, language ranking or production-safety claim. Independent linguistic/domain review, native-authored paraphrases, more families, held-out evaluation and competent-model screening are required before a stronger study. Do not revise these cases or prompts based on pilot outputs and call the revised set held out.
