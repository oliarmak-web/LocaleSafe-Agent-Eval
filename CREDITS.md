# Credits and contribution record

## Creator

**Olivia Iarmak — creator and maintainer.** Olivia originated LocaleSafe, supplied its service-agent use cases and multilingual safety questions, set the research priorities, and directed its development.

Code, scenario drafts, translations, experiment tooling, analyses and documentation were developed with AI assistance under her direction.

## Project artifacts

| Artifact | Evidence | Status |
|---|---|---|
| Original prototype and problem framing | [History](docs/HISTORY.md) | 2025 prototype; new research implementation dated 2026 |
| Service-workflow evaluator | [Scoring specification](docs/SERVICE_SCORING.md) and `localesafe/service_eval.py` | Implemented with synthetic controls |
| Matched workflow study | [Study](docs/WORKFLOW_STUDY.md) and archived source/outputs | 1,800 recorded model decisions; exploratory |
| English rerun control | [Analysis](docs/CONSISTENCY_CONTROL.md) | Reproducible post-hoc analysis; no additional model calls |
| Permission-handoff study | [Technical report](docs/HANDOFF_TECHNICAL_REPORT.md) and [protocol](experiments/handoff-study/PROTOCOL.md) | 2,880 initial model calls; 384 exploratory monitor calls; cached routing replay |

Additional archived experiments include 1,920 Mistral/Phi development calls, a 256-call prompt-format follow-up and a separate 720-call enterprise-sales pilot. Further language-pair diagnostics archive 1,680 Hindi-pair calls, 864 switch-location calls and 336 counterbalanced operation-choice calls. These reuse four draft templates. The SQLite order controls are injected engineering tests, not model experiments. See the [README](README.md) for results and links to each protocol.

Archived source snapshots preserve the implementation used for each experiment.

## External work

The experiments use Qwen, SmolLM3, Mistral and Microsoft Phi model weights. Model identifiers, pinned revisions and weight hashes are recorded in the experiment artifacts; upstream model licenses apply separately from this repository MIT license. Python, PyTorch, Transformers, GitHub and Colab are supporting tools, not project collaborators or endorsers.

Multilingual tool evaluation, consent checks, memory provenance and monitor assessment have prior work. See the [related-work comparison](docs/COMPETITIVE_LANDSCAPE.md) and [originality review](docs/ORIGINALITY_AND_AUTHORSHIP.md). We do not claim to have invented these areas.

## Review status

Translations and reference labels remain development drafts. Independent bilingual review and peer-reviewed validation have not been completed.

Software citation metadata is available in [CITATION.cff](CITATION.cff).

## Domain and public-audio follow-ups

The cross-domain feasibility suite archives 1,440 Qwen/Phi calls on 180 translated draft rows under five fictional policies. Six shared intent families are not 180 independently authored situations. [Findings](docs/DOMAIN_FINDINGS.md).

The separate 40-call local transcription smoke test uses openai/whisper-small and 20 recordings from **Google FLEURS** and **PolyAI MINDS-14**. These recordings and released reference transcriptions are external CC-BY-4.0 data, not original LocaleSafe recordings or MIT-licensed project data. Raw audio remains in ignored local artifacts; archived sample metadata/reference text retains per-source attribution. See [dataset/model sources](experiments/audio-pilot/DATA_SOURCES.md) and the [post-collection reference audit](experiments/audio-pilot/REFERENCE_AUDIT.md). No voice provider endorses the project.
