# Free public-audio transcription smoke test

Frozen October 27, 2026 before ASR inference. This is a separate pipeline smoke test, not a voice-agent benchmark, industry deployment test or cultural assessment.

## Public recordings and selection

Google FLEURS, conversion revision `168de341b3db6859a9bac1c50a2ef5e3b47647e0`: test parquet for en_us, es_419, hi_in, pt_br, cmn_hans_cn and ta_in. PolyAI MINDS-14, conversion revision `0c617db2d3e8c3576abdd7548af4a9f5ff41d2cb`: train parquet for en-US, es-ES, pt-PT and zh-CN. Both publishers declare CC-BY-4.0. MINDS Portuguese is European Portuguese, not Brazilian. MINDS has no Hindi/Tamil condition here.

Use file order and select the first two eligible clips per configuration: nonempty reference; 1–20 seconds; no seven-or-more consecutive digits or email in the reference. MINDS clips must cover two distinct intent-class IDs in their encountered order. Record every prior skip, source parquet SHA256, row index and original audio hash. No selection based on recognition outputs. **20 clips and 40 planned ASR calls.** References come from the released datasets and lack independent review by LocaleSafe. Consent basis is public dataset release, not a claim that individual consent records were inspected.

FLEURS provides read speech; MINDS provides banking-intent speech. Contents, speakers, locales and recording conditions differ. This is not matched-language content or contamination-resistant held-out data; MINDS uses its released train split. Two clips per configuration cannot support a stable ranking, significance or industry-wide conclusion. These recordings do not enact the authored five-domain permission scenarios.

## Model and decoding

Use local CPU only, float32, four torch threads, Transformers 4.57.6, openai/whisper-small at revision `973afd24965f72e36ca33b3055d56a652f456b4d`. Safetensors SHA256 `1d7734884874f1a1513ed9aa760a4f8e97aaa02fd6d93a3a85d27b2ae9ca596b`. Download public files without credentials; no inference API, paid provider or GPU substitution.

For each clip compare automatic language detection against a supplied correct language code. Keep task=transcribe, greedy generation, beam one, no timestamps and 128-new-token cap. Deep-copy generation settings per call to prevent one language setting carrying into the next. Shuffle all 40 clip/arm jobs with seed 20261027. Preserve token IDs, raw decoded transcript, runtime, input waveform hash and settings. No output repair or reruns chosen by quality.

Decode original audio with soundfile float32, average channels if needed and resample to 16kHz using scipy.signal.resample_poly with integer up/down factors. Preserve original bytes and record the processed waveform hash. Language labels en/es/hi/pt/zh/ta come from dataset configurations, not inferred speaker identity.

## Measurement

Report Unicode-code-point character error rate (CER), using real Levenshtein edit distance. Normalize NFKC, casefold, remove punctuation and whitespace. Preserve symbols, digits and combining marks after normalization. Aggregate edit counts over reference character counts per corpus/config/arm. This is not word error rate, grapheme accuracy, semantic accuracy or intent preservation. Do not score Chinese by whitespace word counts or equate a transcript mismatch with a wrong agent action. Record outputs lacking EOS at the decode budget separately.

Compare arms within the same clips; corpus/language totals are descriptive only. Do not attribute differences between languages to language alone. There is no task-action or clinical/financial decision in this pilot, and no ElevenLabs or Wispr product is called. Public model/data licenses and source attributions remain separate from the toolkit's MIT license. Raw audio stays in ignored local artifacts; pinned-source retrieval and hashes make the selected packet reproducible.
