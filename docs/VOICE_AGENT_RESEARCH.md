# Voice-agent signals and next diagnostic tests

Source review: October 27, 2026. Vendor documentation describes capabilities and evaluation priorities; it does not independently establish deployed reliability or market-wide failure rates.

## Why test English–Hindi switching?

[Sarvam's conversation settings](https://docs.sarvam.ai/voice-agents/build/conversation-settings) expose language switching during a call, including English and Hindi. Its [platform overview](https://docs.sarvam.ai/voice-agents/overview) describes Indian-language agents handling code-mixed speech, alphanumerics and proper nouns. [ElevenLabs' language settings](https://elevenlabs.io/docs/eleven-agents/customization/voice/customization/language) also support automatic language switching. These are concrete product signals that language transitions are relevant to agent builders, rather than evidence that any provider fails our tasks.

LocaleSafe's [Hindi-pair protocol](../experiments/hindi-pair/PROTOCOL.md) tests the downstream **text** handoff first. It cannot evaluate speech recognition, spoken pronunciation, latency or interruption detection.

[Vapi's testing documentation](https://docs.vapi.ai/test/voice-testing) separates next-decision text evaluations from full-conversation simulations and voice tests. This supports a layered design: establish the text decision first, then test transcription and turn-taking separately.

## Related work limits the novelty claim

[ServiceNow AI's code-switching study](https://huggingface.co/blog/ServiceNow-AI/code-switching) evaluates enterprise speech recognition and downstream comprehension, with native-speaker review. [CoSE-E](https://arxiv.org/abs/2609.35645) also studies enterprise code-switched ASR and operational impact. These are close precedents for the proposed audio work; language switching and downstream error propagation are not new research topics by themselves. LocaleSafe's current bounded extension compares the same permission-change tasks across language pairs and separates handoff records, actor actions and permission-monitor judgments. Adding Hindi alone does not establish methodological novelty.

## Highest-value follow-ups

| Test | Concrete industry situation | How to locate the failure |
|---|---|---|
| Corrected identifiers and amounts | A telecom caller corrects an account suffix or service plan after switching languages | Compare clean transcript, human-verified transcript of audio and actual ASR output; score exact entities and final sandbox action separately |
| Withdrawal during interruption | A caller says to stop a previously approved service change while the agent is speaking | Measure when audio, transcript, agent state and executor each receive the withdrawal; distinguish recognition, timing and stale permission failures |
| Product facts versus customer language | A cybersecurity buyer asks in Hindi about an English capability document | Cross buyer language with document language while holding product facts fixed; score extraction, unsupported claims and reasons separately |
| Human transfer fidelity | A financial-services support assistant transfers a disputed-charge inquiry to a specialist | Compare the complete history, generated handoff and reviewed reference record; check amount, negation, requested next step and permission without making credit or fraud determinations |

First establish competence on clean text in each language. Then introduce audio as a separate factor using licensed recordings and independent review. Synthetic transcript corruption is an engineering stress test, not an actual ASR measurement. Evaluate Romanized Hindi and Hinglish separately from Devanagari Hindi. Names, numbers, negation and correction deserve exact checks even when a transcript's overall similarity looks good.

[Sarvam's speech-to-text page](https://www.sarvam.ai/speech-to-text) describes entity preservation and intent alongside word-error rate. That supports investigating task-critical meaning rather than transcript similarity alone; its vendor-reported claims are not LocaleSafe results.

All examples above are proposed tests. No voice-provider experiment, real call, medical decision, financial eligibility decision or production integration has been conducted here. Language alone must not stand in for nationality, business geography or regulatory policy.
