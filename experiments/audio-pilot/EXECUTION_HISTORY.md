# Execution history

October 27, 2026. Source/selection protocol frozen in `61f055b`; local CPU collector frozen in `8151a42`. Public recording selection completed before ASR inference: 20 clips, 213.9 seconds, 8,969,806 original audio bytes. Input manifest SHA256 `4b35dfcaefc569cb1285500d8c9a60a0548b74e140d6d0d44438d6acf3b458c5`. Original audio remains under ignored reports/public-audio-packet; pinned-source retrieval reproduces it.

The first collector launch failed on missing scipy before output-directory creation or model inference. Installing the public dependency resolved setup; code, clip selection and decoding protocol were unchanged. The subsequent local CPU run completed all 40 calls. No failed model outputs were replaced. Raw run: experiments/results/audio-whisper-small-20261027; derived results: experiments/analysis/audio-pilot/summary.json.

The pinned safetensors hash was verified before inference. Internal archive hashes, job order, source snapshots, settings, all 20 original audio hashes, scores, feature identity across paired arms and decode-budget flags passed audit. Native tokenizer decoding of all 40 stored token sequences reproduced the raw outputs; independently regenerated waveform and input-feature hashes also matched. This audit reran preprocessing/token decoding, not model inference.

All 20 auto/provided-language pairs had identical decoded text and token sequences. The MINDS reference provenance issue was found during post-collection source review and recorded in REFERENCE_AUDIT.md. Original reference strings, metrics and model outputs were retained. MINDS ratios describe disagreement with released ASR hypotheses, not validated human-gold error. No cultural, deployment or voice-product claims are supported.

No paid API, ElevenLabs, Wispr account, microphone recording or private customer data was used. Model runtime: CPU float32, torch 2.14.1+cpu, Transformers 4.57.6; remaining versions are in the manifest. The public-data/model sources are attributed in DATA_SOURCES.md. Individual participant consent records were not independently reverified.
