# Credits and contribution record

## Creator

**Olivia Iarmak — creator and maintainer.** Olivia originated LocaleSafe, supplied its service-agent use cases and multilingual safety questions, set the research priorities, and directed its development. She authorized the current direction on permission changes across multilingual handoffs.

Code, scenario drafts, translations, experiment tooling, analyses and documentation were developed with AI assistance under her direction. Specific methods and the newer protocol were drafted with that assistance. This is not a claim that every line or research detail was independently written by Olivia.

## Project artifacts

| Artifact | Evidence | Status |
|---|---|---|
| Original prototype and problem framing | [History](docs/HISTORY.md) | 2025 prototype; new research implementation dated 2026 |
| Service-workflow evaluator | [Scoring specification](docs/SERVICE_SCORING.md) and `localesafe/service_eval.py` | Implemented with synthetic controls |
| Matched workflow study | [Study](docs/WORKFLOW_STUDY.md) and archived source/outputs | 1,800 recorded model decisions; exploratory |
| English rerun control | [Analysis](docs/CONSISTENCY_CONTROL.md) | Reproducible post-hoc analysis; no additional model calls |
| Permission-handoff prototype | [Protocol](experiments/handoff/PROTOCOL.md) | Implemented draft cases and synthetic controls; model study pending |

Git history records development, not proof that every idea is novel or that a particular person manually wrote every line. Archived source copies preserve reproducibility and are not separate contributions.

## External work

Qwen supplied the evaluated model weights; their licenses and revisions are recorded in the experiment artifacts. Python, PyTorch, Transformers, GitHub and Colab are supporting tools, not project collaborators or endorsers.

Multilingual tool evaluation, consent checks, memory provenance and monitor assessment have prior work. See the [related-work comparison](docs/COMPETITIVE_LANDSCAPE.md) and [originality review](docs/ORIGINALITY_AND_AUTHORSHIP.md). We do not claim to have invented these areas.

## Reviews and recognition

No independent bilingual review, peer-reviewed publication, external adoption, citation impact or media coverage has been verified in this repository. Add named reviewers only after they perform the work and consent to attribution. Record their exact contribution and the artifact version reviewed.

Use [CITATION.cff](CITATION.cff) for software attribution. Authorship, methodological novelty and external significance are distinct claims; this record supports attribution, not a finding of field-wide impact.
