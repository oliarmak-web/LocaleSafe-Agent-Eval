# Public recording sources and attribution

Audio and source transcriptions are third-party data, not original LocaleSafe recordings and not covered by the toolkit's MIT license. The publishers list **Creative Commons Attribution 4.0**; retain their attribution and identify preprocessing or derived analyses. [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).

- **Google FLEURS**, [dataset and citation](https://huggingface.co/datasets/google/fleurs), [FLEURS paper](https://arxiv.org/abs/2205.12446). Selected released read-speech clips from English US, Latin American Spanish, Hindi, Brazilian Portuguese, Mandarin Simplified Chinese and Tamil configurations. Conversion revision is pinned in the retrieval script and sample manifest.
- **PolyAI MINDS-14**, [dataset and citation](https://huggingface.co/datasets/PolyAI/minds14), [MINDS paper](https://arxiv.org/abs/2104.08524). Selected banking-intent recordings from English US, Spanish Spain, Portuguese Portugal and Mandarin Chinese. European Portuguese must not be relabeled Brazilian Portuguese.

The local packet retains original audio bytes, source parquet hashes, row indices, source references and per-clip hashes. It excludes dataset gender labels from analysis. Public-release licensing is the provenance basis; individual participant consent records have not been independently inspected by LocaleSafe. References and acoustic naturalness have not received new native-speaker review.

The transcription baseline uses [openai/whisper-small](https://huggingface.co/openai/whisper-small), whose published Hugging Face model card lists Apache-2.0. Its exact revision and safetensors hash are frozen in PROTOCOL.md. The authors/model provider do not endorse LocaleSafe. The model is run locally; no OpenAI inference API is used.

Neither corpus represents the five authored domain workflows, a population of callers or cultural communication styles. Source and model licenses remain upstream; this file is provenance, not a certification of every source recording's rights or consent.
