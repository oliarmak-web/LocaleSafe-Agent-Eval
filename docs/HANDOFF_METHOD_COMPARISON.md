# Handoff study: comparison with the closest methods

Review dated October 22, 2026. The comparison uses the cited methods and limitations sections; it is not a claim that the entire literature has been exhausted. No external code, prompts or datasets were imported.

| Prior work reviewed | Established contribution | LocaleSafe's bounded comparison |
|---|---|---|
| [EAL-Bench, sections 3.1–3.3 and 4.6](https://arxiv.org/html/2609.01836v1) | Separates memory formation from downstream propagation; uses deterministic authority, faithful-memory controls, typed/text memory and repairs | Crosses four English/Spanish conversation patterns with generated text/records, an oracle record, actor decisions and fixed-action monitor verdicts |
| [MasDrift, sections 3.3–3.4](https://arxiv.org/html/2608.07556v3) | Compares authorization preservation across coordination architectures and separates task utility from authorization behavior | Holds the bounded workflow fixed; varies evidence and language pattern. It does not compare multi-agent architectures or long-horizon delegation |
| [Root-scoped revocation, sections 7.2–7.3](https://arxiv.org/html/2609.21284v1) | Tests late effects, endpoint fences, root cuts and revocation under asynchronous execution | Tests sequential permission updates in an in-memory sandbox. It does not establish distributed closure, race safety or cryptographic authorization |
| [COAI recorded-trajectory monitoring](https://www.coairesearch.org/research/agent-monitoring/report/) | Compares monitor decisions with varied language and evidence histories | Adds generated handoffs and actor outcomes from the same authored cases, with independent fixed-action probes and a monitored record contract |

EAL-Bench's controls and formation/propagation distinction are substantial precedents. A perfect-record control, structured memory or a schema validator is not a new concept in isolation. Searches within the inspected EAL-Bench and MasDrift HTML did not locate a multilingual factor; this is a limited observation, not proof that no related artifact or paper includes one.

## Current empirical contribution

LocaleSafe supplies a reproducible English/Spanish experiment record that separates current permission preservation, requested-action representation, action selection and monitor judgment. Its observed failure pathway is narrower than “translation loses permission”: Qwen3-4B preserved the permission fields in these runs while actor and monitor outcomes still changed with the evidence format.

The value is the specific diagnosis and matched evidence, not a claim to have invented multilingual evaluation or authorization monitoring. The study includes negative evidence for a simple language-switch explanation and retains a second model that failed the competence screen.

## Remaining limits

Draft translations, eight templates, two small models and a shared-model role configuration limit generalization. Only one model qualified for the reserved evaluation families. A reviewed bilingual extension and independent reproduction are required before making broader claims. The monitor intervention and cached routing analysis were designed after inspecting results and remain exploratory.
