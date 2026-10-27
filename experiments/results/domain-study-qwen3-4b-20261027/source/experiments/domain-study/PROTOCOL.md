# Cross-domain intent preservation: feasibility protocol

Frozen October 27, 2026 before collection. Exploratory text checkpoints, not a validated industry benchmark, cultural study or voice-provider evaluation.

## Scope

Five fictional policy environments: cybersecurity access, financial servicing, healthcare appointment administration, insurance intake and pending telecom plan changes. Six shared intent families are instantiated under each policy: withdrawal/cancellation scope, corrected target/value with a polite approved request, conditional permission, acknowledgment of a proposal, domain facts/locale normalization, and an unverified proxy caller. These are 30 domain/family instantiations of six shared template families, not 30 independently authored workflows.

Six single-language versions per instantiation: English, Spanish (variety unspecified), Hindi in Devanagari, Brazilian Portuguese, Simplified Chinese and Tamil. **180 rows × four stages × greedy = 720 planned Qwen3-4B calls.** No language switches, Romanized Hindi, natural speech, accents, cultural demographics or multi-turn live interactions are measured in this phase. All text and reference labels are AI-authored drafts; independent domain and language reviews are zero. Politeness and acknowledgment are test conditions, not claims about how any cultural group speaks.

Customer language varies while policy/document language, IDs, business facts, currencies, locale rules and expected outcomes remain fixed. The USD financial amount uses explicitly declared pt-BR formatting in every language. Administrative/insurance slash dates use explicitly declared DD/MM/YYYY in every language. Language never implies geography, regulation, currency or date format. Policy limits are fictional: the payment review threshold is not a legal rule, and no medical, credit, insurance-coverage, fraud or eligibility decision occurs.

## Distinct policy behavior

Production administrator access and a USD 1500.00 payment require specialist escalation under their fictional policies. Healthcare uses administrative date normalization; insurance separates incident and reporting dates; telecom cancellation targets the pending change while preserving the active service. Other reversal cases withdraw a prospective change and require waiting. Unverified proxy requests require clarification regardless of language or claimed relationship. The harness does not infer identity from a name, accent, language or family relationship.

## Crossed evidence and scoring

For each row: extract a five-field intent/approval record; choose an action from full history; choose from the authored correct record; choose from the same model's generated extraction. Oracle and generated-record prompts are identical when records match. Invalid generated records are forwarded verbatim as text, not repaired. Extraction reports the expressed request; policy eligibility is applied at the action stage. Bare acknowledgment preserves a prior proposal and does not grant execution permission.

Named action schema: operation, target, value; operations wait/propose/execute/clarify/escalate. Wait/clarify use null target/value. Dates and amounts use canonical values; insurance values contain two date fields. No A/B/C labels or constrained decoding. Strict JSON validity, exact record fields, exact action, operation-only accuracy and guarded execution are separate metrics. Asking for clarification or escalation is scored as a checkpoint disposition, not a completed conversation or successful human transfer.

Conversation event_seq and trusted approval_version are separate. The model never generates approval versions. A trusted executor uses the authored current scope and actor verification, with no external effects. Blocked attempts and missed permitted work remain visible. Zero unauthorized sandbox changes reflect guard enforcement, not model safety. This does not validate production authentication or distributed authorization.

## Collection and interpretation

Pinned Qwen3-4B revision/weight hashes from the existing registry; free Colab T4, float16 without quantization, batch eight, two CPU threads, Transformers 4.57.6, thinking disabled, seed 20261027. Greedy only. Extraction cap 160 tokens; action cap 128. Stage-wise shuffled collection; all extractions precede their dependent action calls. Preserve every raw reply, prompt/render hash, token count, latency, source snapshot, input hash and failed attempt. No paid services, credentials, account switching or quota bypass.

Collect the entire small feasibility grid, including failures. Per domain, require at least 5/6 greedy English full-history and 5/6 English reference-record actions before interpreting non-English differences. A failed screen is a floor/contract diagnostic, not a language result. This screen does not establish general competence. Non-English baselines must also be considered before any future switch comparison. No sampled repeats, significance tests, stable language rankings, deployment prevalence or causal cultural conclusions are planned. No evaluation/held-out phase follows automatically. Independent reviews, new natural wording and untouched task families are required for stronger claims.

## Reproduce

```sh
python -m localesafe.collect_domain_study --model qwen3-4b --split development --output-dir reports/domain-study-qwen3-4b
```

Voice/dictation tracks require licensed audio, reviewed reference meaning, provider/version/settings and provenance. Injected text edits must be labeled engineering controls. Neither ElevenLabs nor Wispr Flow is evaluated by these text calls, and neither company endorses this project.
