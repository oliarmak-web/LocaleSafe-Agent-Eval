# Intent preservation across service workflows

Five fictional policy environments now share a text-checkpoint protocol in six languages. The goal is to locate failures in expressed intent, approval, domain facts, handoffs and policy application. This is a draft feasibility suite, not a validated industry benchmark or cultural assessment.

| Domain | Concrete boundary |
|---|---|
| Cybersecurity access | Staging access versus production administrator access requiring specialist review |
| Financial servicing | Discussing a proposal, withdrawing a payment and normalizing a declared-format amount; fictional specialist threshold |
| Healthcare administration | Administrative appointment dates and unverified proxy requests; no clinical decision |
| Insurance intake | Incident date versus reporting date, with existing records retained; no coverage determination |
| Telecom | Cancelling a pending plan change while keeping the active service intact |

The common conditions include corrections, polite approved requests, conditional permission, acknowledgment without execution approval, domain facts and caller verification. Policies, currency and locale rules stay fixed when customer language changes. These fixtures instantiate six shared templates under five policies; repeated translations do not create independent situations. No native-speaker or industry review has occurred.

The new contract separates conversation sequence from trusted approval versions and uses named actions rather than choice letters. These are design changes motivated by earlier confounds, not isolated or validated fixes. Two 720-call runs are complete; see the [findings](DOMAIN_FINDINGS.md) and [model comparison](DOMAIN_COMPARISON.md). [Frozen protocol](../experiments/domain-study/PROTOCOL.md) · [Execution status](../experiments/domain-study/EXECUTION_HISTORY.md).

## Try the checkpoints locally

Python 3.11+, no API key or model download for export and scoring:

```sh
python -m localesafe.domain_eval --reference-demo --output reports/domain-reference.json
python -m localesafe.domain_eval --export-prompts --language en --output reports/domain-prompts-en.jsonl
```

The first command scores 180 authored reference actions: expected 180 correct and zero unauthorized attempts. These are injected examples, not model results. The second exports 30 English checkpoints across five policies. Send only each row's messages to an agent; retain case_id outside the prompt to join results. Produce JSONL replies with exactly case_id and raw_output (the untouched model reply as a string), then score:

```sh
python -m localesafe.domain_eval --traces private/agent-replies.jsonl --trace-origin model --language en --output reports/domain-agent-en.json
```

All outputs require new filenames. Missing replies count as failures; duplicate/unknown IDs are rejected. The report separates format, exact action, operation choice, rejected execution attempts and mock final state. It does not call an API or prove where supplied traces came from. These rules and draft fixtures need independent validation before use as deployment criteria.

## Voice and dictation: separate evidence tracks

For a future ElevenLabs-style agent test, compare reviewed intended meaning, actual ASR transcript, generated intent record and final action. For a Wispr Flow-style dictation test, compare reviewed meaning with the delivered text before evaluating any downstream action. A polished paraphrase is not inherently an error; losing negation, scope, conditions, entities or corrections can change intent. Natural interruptions also need timestamps and executor timing, beyond text checkpoints.

[Wispr's limitations documentation](https://docs.wisprflow.ai/articles/4048537120-what-to-expect-from-flow-accuracy-and-known-limitations) distinguishes formatting from mishearing and discusses mixed-language behavior. [ElevenLabs' language documentation](https://elevenlabs.io/docs/eleven-agents/customization/voice/customization/language) describes language configuration and detection. Platform, model, language settings and mode must be recorded; vendor capabilities are not LocaleSafe results or endorsements.

No ElevenLabs/Wispr calls, private customer recordings or spoken-culture findings are included. A separate [free public-recording smoke test](PUBLIC_AUDIO_QUICKSTART.md) has 40 local ASR outputs on unrelated released corpus clips; it does not explain the authored domain-task failures. Free provider access and appropriate licensed recordings are not assumed. The local intake tool validates provenance before an audio study:

```sh
python -m localesafe.speech_evidence private/speech-evidence.json --audio-root private/audio --output reports/speech-intake.json
```

Keep recordings and private manifests outside Git. The envelope has format_version 1 and a records list. Each record declares an ID, case_id from the domain suite, source_kind (human_reference/asr_output/dictation_output/injected_text_control), provider, provider_version, settings, review_status, reviewer_id and aligned events. Each event declares event_seq, transcript, audio_file, audio_sha256, audio_origin, license and consent. Audio paths are relative to the supplied root. Human recordings require documented consent; synthetic recordings remain labeled synthetic. Independent review declarations require reviewer attribution. These metadata checks do not verify the truth of the declarations.

Injected edits use null audio fields and remain engineering controls, never ASR observations. The tool does not upload files, call a provider or establish clinical, financial or production safety. No culture is inferred from a language, name or relationship. Native-authored wording and independent review are requirements before cultural interpretations.
