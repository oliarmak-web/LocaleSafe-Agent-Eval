# Research index

Start with the five-domain findings. Use the reproduction guide to audit recorded outputs or export checkpoints for your own agent. This page is the directory of evidence; detailed results stay in the linked reports.

[Reproduction guide](QUICKSTART.md) · [Project overview](../README.md) · [Research brief](RESEARCH_BRIEF.md)

## Main experiments

| Study | Question and scope | Recorded calls | Findings and tables | Protocol |
|---|---|---:|---|---|
| Five-domain checkpoints | Intent, policy and actions across six languages and two models; six shared intent families under five fictional policies | 1,440 | [Findings](DOMAIN_FINDINGS.md) · [Comparison](DOMAIN_COMPARISON.md) · [Qwen](DOMAIN_QWEN_RESULTS.md) · [Phi](DOMAIN_PHI_RESULTS.md) | [Frozen protocol](../experiments/domain-study/PROTOCOL.md) · [Replication](../experiments/domain-study/MODEL_REPLICATION.md) |
| Cybersecurity sales pilot | Buyer requirements versus product-fit decisions and reasons; six situations, five languages, two models | 720 | [Findings](SALES_PILOT_FINDINGS.md) · [Tables](SALES_PILOT_RESULTS.md) | [Frozen protocol](../experiments/sales-pilot/PROTOCOL.md) |
| Permission handoffs | Full conversation versus generated handoffs; action and monitor scores on draft English/Spanish cases | 2,880 | [Technical report](HANDOFF_TECHNICAL_REPORT.md) · [Tables](HANDOFF_RESULTS.md) | [Frozen protocol](../experiments/handoff-study/PROTOCOL.md) |
| Monitor intervention | Added rules versus baseline and authored correct records; exploratory follow-up on inspected cases | 384 | [Results and trade-offs](MONITOR_FOLLOWUP.md) | [Frozen protocol](../experiments/monitor-followup/PROTOCOL.md) |
| Additional model screens | Mistral and Phi development replication; both failed the original English qualification screen | 1,920 | [Results](MODEL_EXTENSION_RESULTS.md) | [Replication protocol](../experiments/handoff-study/MODEL_EXTENSION.md) |
| Prompt-format control | Change only the presentation of tool examples; inspect gains and regressions | 256 | [Results](FORMAT_FOLLOWUP.md) | [Frozen protocol](../experiments/format-followup/PROTOCOL.md) |
| English/Hindi comparison | Single-language requests and both switching directions, compared with English/Spanish; four shared templates | 1,680 | [Findings](HINDI_PAIR_FINDINGS.md) · [Tables](HINDI_PAIR_RESULTS.md) | [Frozen protocol](../experiments/hindi-pair/PROTOCOL.md) |
| Public-audio baseline | Automatic versus supplied language in local Whisper-small; 20 unrelated public corpus clips | 40 | [Results](AUDIO_SMOKE_RESULTS.md) · [Reference audit](../experiments/audio-pilot/REFERENCE_AUDIT.md) | [Frozen protocol](../experiments/audio-pilot/PROTOCOL.md) |

Counts include repeated conditions and translations, not independent situations. These studies use different cases and contracts; their scores are not a pooled leaderboard. The five-domain suite's 180 rows are translations of six shared intent families instantiated under five policies. All translations and domain policies require independent review.

## Diagnostic controls and earlier studies

| Study | What it established in this setup | Evidence |
|---|---|---|
| Switch location: 864 calls | The English screen failed because of older approval versions; the synthetic version rule limits language attribution | [Findings](SWITCH_BOUNDARY_FINDINGS.md) · [Tables](SWITCH_BOUNDARY_RESULTS.md) · [Protocol](../experiments/switch-boundary/PROTOCOL.md) |
| Operation choice: 336 calls | Answer order changed correctness in every case; reducing output complexity did not isolate comprehension | [Findings](OPERATION_PROBE_FINDINGS.md) · [Tables](OPERATION_PROBE_RESULTS.md) · [Protocol](../experiments/operation-probe/PROTOCOL.md) |
| Saved approvals and retries: 21 injected controls | Approval checks and retry deduplication prevented some effects, but corrected requests still needed replanning; zero model calls | [Results](ORDER_CONTROLS.md) · [Protocol](../experiments/order-controls/PROTOCOL.md) |
| Permission-guard demonstration: 48 injected cases per trace | All 48 stale-permission attempts were blocked; this demonstrates code enforcement, not model reliability | [Local demonstration](QUICKSTART.md#1-understand-a-permission-failure) · [Fixture protocol](../experiments/handoff/PROTOCOL.md) |
| Earlier five-language workflow study: 1,800 decisions | Format compliance did not imply correct tool arguments; translating policy did not consistently improve results | [Findings](FINDINGS.md) · [Workflow study](WORKFLOW_STUDY.md) · [English rerun control](CONSISTENCY_CONTROL.md) |
| Earlier pilots and attribution probes | Direct responses, format effects, answer-position sensitivity and preserved interrupted attempts | [Historical experiment guide](../experiments/README.md) |

Switch-location and operation-choice controls reuse the Hindi study's four draft templates. More calls do not add independent scenario families. Failed gates, invalid outputs and evaluation confounds remain part of the evidence.

## Run, review or extend

- **Reproduce recorded results:** [standard-library replay commands](QUICKSTART.md#2-verify-the-recorded-model-experiments).
- **Evaluate your agent:** [five-domain prompt export and scoring](DOMAIN_AND_SPEECH_STUDY.md#try-the-checkpoints-locally). Preserve untouched replies and separate model outputs from injected fixtures.
- **Review a language or policy:** [review guide](LANGUAGE_REVIEW_GUIDE.md). Accepted corrections require a new version; frozen cases and results remain intact.
- **Retrieve public recordings:** [audio quickstart](PUBLIC_AUDIO_QUICKSTART.md) and [third-party sources/licenses](../experiments/audio-pilot/DATA_SOURCES.md). MINDS references are machine-generated hypotheses, not verified gold.
- **Understand proposed voice work:** [voice-agent research](VOICE_AGENT_RESEARCH.md). Proposed provider, interruption and cultural tests are not completed product evaluations.
- **Contribute:** [contribution guide](../CONTRIBUTING.md) and [security guidance](../SECURITY.md).

## Where information lives

| Location | Contents |
|---|---|
| `docs/` | Findings, interpretations, instructions and research context |
| `experiments/` study folders | Frozen protocols, case designs and execution histories |
| `experiments/results/` | Archived outputs, source snapshots, manifests and hashes; unsuccessful attempts remain preserved |
| `experiments/analysis/` | Derived machine-readable summaries |
| `localesafe/` and analysis scripts in `experiments/` | Evaluators, collectors and reproducible scoring |
| `reports/` | Ignored local replay outputs, downloads and generated files; not the committed evidence archive |
| `private/` | Ignored local inputs and model files; do not commit credentials or customer data |

Per-study execution histories document interruptions and recovery: [domains](../experiments/domain-study/EXECUTION_HISTORY.md), [sales](../experiments/sales-pilot/EXECUTION_HISTORY.md), [handoffs](../experiments/handoff-study/EXECUTION_HISTORY.md), [format control](../experiments/format-followup/EXECUTION_HISTORY.md), [Hindi](../experiments/hindi-pair/EXECUTION_HISTORY.md) and [audio](../experiments/audio-pilot/EXECUTION_HISTORY.md).

## Methods, provenance and citation

The toolkit separates fact extraction, exact action correctness, output contracts, permission and monitor judgments. An authored correct record is a diagnostic control, not a demonstrated automatic fix. A guard blocking a command is not evidence that the model chose safely.

[Method comparison](HANDOFF_METHOD_COMPARISON.md) · [Related work](COMPETITIVE_LANDSCAPE.md) · [Benchmark registry](BENCHMARKS.md) · [Authorship and provenance](../CREDITS.md) · [Project history](HISTORY.md)

Cite Olivia Iarmak, LocaleSafe, with the exact experiment and commit used. [CITATION.cff](../CITATION.cff) · [BibTeX](../CITATION.bib). Cite external models and datasets separately. No DOI, peer-reviewed validation or deployed safety claim is implied.
