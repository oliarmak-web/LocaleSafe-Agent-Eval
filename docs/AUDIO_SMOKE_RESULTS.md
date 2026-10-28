# Free public-audio transcription smoke test

20 public clips, 40 local CPU Whisper-small transcriptions. Two clips per dataset configuration; no confidence intervals, ranking, cultural or deployed-product conclusions.

Ratios are character-edit distance to released references. **MINDS references are ASR hypotheses, not verified human gold; its ratios measure transcript disagreement.**

| Dataset | Configuration | Automatic-language edit ratio | Supplied-language edit ratio |
|---|---|---:|---:|
| PolyAI/minds14 | en-US | 26/65 (40.0%) | 26/65 (40.0%) |
| PolyAI/minds14 | es-ES | 173/185 (93.5%) | 173/185 (93.5%) |
| PolyAI/minds14 | pt-PT | 40/196 (20.4%) | 40/196 (20.4%) |
| PolyAI/minds14 | zh-CN | 11/30 (36.7%) | 11/30 (36.7%) |
| google/fleurs | cmn_hans_cn | 15/44 (34.1%) | 15/44 (34.1%) |
| google/fleurs | en_us | 5/169 (3.0%) | 5/169 (3.0%) |
| google/fleurs | es_419 | 1/233 (0.4%) | 1/233 (0.4%) |
| google/fleurs | hi_in | 112/252 (44.4%) | 112/252 (44.4%) |
| google/fleurs | pt_br | 9/312 (2.9%) | 9/312 (2.9%) |
| google/fleurs | ta_in | 40/171 (23.4%) | 40/171 (23.4%) |

Supplying language lowered edit count on 0/20 clips, increased it on 0/20 and tied on 20/20.

Decoded outputs matched exactly across arms on 20/20 clips; token sequences matched on 20/20.

CER uses Levenshtein Unicode-code-point edits after NFKC/casefold and removal of punctuation/whitespace. It is not word error rate or semantic correctness. Scripts, content, speakers and recording conditions differ; cross-language percentages are not a controlled language comparison.

FLEURS uses released read speech. MINDS-14 uses released banking-intent speech; its [source paper](https://arxiv.org/html/2104.08524) describes Google ASR-generated transcriptions. Reference errors or omissions can affect the ratios, so larger disagreements are not automatically hallucinations. pt-PT is European Portuguese, while FLEURS pt_br is Brazilian Portuguese. Published references and consent records have not been independently reverified by LocaleSafe. No ElevenLabs, Wispr Flow or downstream agent was evaluated. Source audio stays in ignored local artifacts; pinned retrieval and per-clip hashes support reproduction.

[Recording sources and licenses](../experiments/audio-pilot/DATA_SOURCES.md) · [Frozen protocol](../experiments/audio-pilot/PROTOCOL.md).
