# Retrieve the free recording packet

The selected packet contains **20 publicly released clips, about 214 seconds**, from Google FLEURS and PolyAI MINDS-14. Recordings and references remain third-party CC-BY-4.0 data; retain [source attribution](../experiments/audio-pilot/DATA_SOURCES.md). Original audio is kept in ignored local artifacts.

From the repository checkout, install retrieval dependencies and choose a new output directory:

```sh
python -m pip install huggingface_hub==0.36.2 pyarrow==26.0.0 soundfile==0.14.0
python -m experiments.fetch_public_audio --output-dir reports/public-audio-packet
```

The command downloads pinned source parquet files and saves audio/, samples.json, original clip hashes, row indices and selection provenance. It calls no inference API and requires no account credentials. MINDS pt-PT is European Portuguese; FLEURS pt_br is Brazilian Portuguese. Hindi and Tamil are covered by FLEURS, not this MINDS selection.

Replay the recorded transcription metrics with standard-library Python:

```sh
python -m experiments.summarize_audio_smoke experiments/results/audio-whisper-small-20261027 --output-dir reports/audio-replay
```

Add --packet reports/public-audio-packet to verify downloaded clip bytes as well. This replays recorded outputs; it does not run a recognizer. Full local inference additionally needs the runtime versions recorded in the [archived manifest](../experiments/results/audio-whisper-small-20261027/manifest.json), including CPU torch, Transformers 4.57.6, NumPy and SciPy. The collector command is:

```sh
python -m localesafe.collect_audio_smoke --packet reports/public-audio-packet --output-dir reports/my-audio-run
```

The completed smoke test used local Whisper-small, a separate open model. ElevenLabs and Wispr Flow were not called. Automatic and supplied-language arms produced identical decoded text on all 20 clips. This does not establish performance on code-switching, interruptions or the authored industry tasks.

MINDS references are ASR-generated hypotheses according to the source paper; edit ratios against them measure disagreement, not human-grounded recognition error. FLEURS references also lack independent review by LocaleSafe. Two clips per configuration cannot support language rankings or cultural conclusions. [Results](AUDIO_SMOKE_RESULTS.md) · [Reference audit](../experiments/audio-pilot/REFERENCE_AUDIT.md).
