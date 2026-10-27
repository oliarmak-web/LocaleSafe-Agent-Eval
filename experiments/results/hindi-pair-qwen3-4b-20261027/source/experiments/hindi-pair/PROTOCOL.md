# English–Hindi versus English–Spanish handoffs

Frozen before collection, October 27, 2026. Exploratory text-only extension; not a reviewed benchmark or voice experiment.

## Question

Does the descriptive switching pattern recur in English–Hindi, after comparing each language with its own single-language baseline? Preserve the original four development templates (withdrawal, changed record, proposal only, changed value), two identifier/value variants, and all original English/Spanish text and labels. Add Hindi in Devanagari. All Hindi text is AI-authored draft with zero independent reviews. No Romanized Hindi, Hinglish, audio, cultural adaptation or regulatory comparison is included.

Seven patterns: en-en, es-es, en-es, es-en, hi-hi, en-hi, hi-en. 56 rows × three decoding profiles × ten calls = **1,680 planned Qwen3-4B calls**. Four authored templates, not 56 independent situations. All conditions are collected together; original archives remain unchanged. Do not pool historical and new repeats as independent cases.

## Fixed method

Use the pinned Qwen3-4B revision, original handoff instructions, strict scorer, 192/96/24 summary/action/monitor token caps, greedy and two sampled profiles, float16 without quantization, batch eight and Transformers 4.57.6. Use the original seed 20261022 and ordering function; language additions change batch composition, so historical output identity is not assumed. Shared seeds do not equate random draws across prompts. Free Colab T4 only; stop on quota denial, do not pay or change accounts. Preserve every failed attempt and source snapshot.

The ten calls are two handoffs (English narrative and structured record), four actor evidence conditions (full history, oracle record, generated record, generated narrative), and four fixed monitor probes (allowed/forbidden × full history/generated record). References remain excluded from ordinary visible history. The trusted guard checks attempted and completed actions separately. Perfect records are diagnostic controls, not multilingual inputs or demonstrated fixes.

Use the unchanged collector with this study's cases/design, through `localesafe.collect_hindi_pair`. This wrapper adds the extension's sources to the archive. No prompt repair, constrained decoding or best-of selection. Do not revise prompts after inspecting results.

## Analysis and stopping rules

Report counts per language pattern, evidence condition and profile. Primary descriptive outcome: greedy full-history action correctness, matched by situation and variant. Report switches against **both** English and the partner-language baseline; do not call any difference a switching penalty without those baselines. Also report record-field fidelity, exact record fidelity, invalid output, unauthorized attempts, monitor false acceptance/blocking and within-pattern sampled-repeat correctness changes. Preserve per-block gains/losses rather than pooling language/profile observations as independent samples.

Repeat the original English competence screen: at least 7/8 greedy correct actions in both full-history and oracle-record conditions. On failure retain the entire development run, report the floor and make no language attribution. Qwen passed historically, but that does not waive this run's screen. No evaluation collection, significance claim, language ranking or causal script claim is planned. Hindi review, native-authored paraphrases, more templates and additional competent models remain necessary for generalization.

## Reproduce collection

```sh
python -m localesafe.collect_hindi_pair --model qwen3-4b --split development --output-dir reports/hindi-pair-qwen3-4b
```

Analysis of recorded calls must remain possible without a GPU. Runtime status belongs in EXECUTION_HISTORY.md; planned calls must never be presented as completed results.
