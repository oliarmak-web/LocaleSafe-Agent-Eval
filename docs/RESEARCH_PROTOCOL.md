# Research protocol — draft, no empirical results yet

## Question

For semantically equivalent requests, how consistently does a fixed agent choose escalation, clarification, and tool arguments across languages? Does an explicit information-checking instruction change those outcomes?

## Baseline release

The current release supplies an evaluator and synthetic fixtures only. Before collecting baseline results:

1. Recruit language reviewers and document semantic equivalence, reviewer provenance/consent, ambiguities, and disagreements. Do not equate textual substitutions with real accents.
2. Define an illustrative assistance policy with domain review. Add diverse urgent, routine, negated, reported, ambiguous, and code-switching scenarios. Avoid personal or real patient data.
3. Freeze a versioned development set and a separately authored private held-out set. Keep every language version of a scenario in the same split. Record dataset and prompt hashes before testing.
4. Select models and languages based on a declared scope, available access, and cost. Record exact model identifiers, dates, prompts, tool schema, decoding settings, retries, seeds where supported, and latency/cost. Do not feed expected answers to the model.
5. Preserve refusals, malformed outputs, timeouts, and all attempts. The current evaluator rejects incomplete artifacts; report collection failures separately rather than silently dropping them. Define this handling before collection.
6. Evaluate observable behavior with independent review of disputed labels. Report sample sizes, paired case outcomes, uncertainty at the scenario-family level, and failures. Repeated generations are nested within scenarios, not independent new scenarios.

## v2: intervention study

Compare the unchanged baseline prompt with one preregistered intervention: check whether required tool arguments are present and request clarification when appropriate. It must not delay a policy-required escalation. Freeze this policy before collection; do not implement a rule that always clarifies.

Hold model/version, cases, tools, and decoding settings fixed. Randomize run order where feasible. Choose repetitions and sample size using pilot variance and a power or precision rationale. Evaluate missed escalation, unnecessary escalation, exact calls, and clarification correctness separately; do not optimize a single opaque safety score. Report added latency, cost, and regressions. Use paired analysis with family-level resampling and distinguish exploratory from confirmatory comparisons. No statistical significance claims from example fixtures.

## Later speech extension

Evaluate real licensed/consented audio and matched reference transcripts separately from downstream agent decisions. Use established word-error-rate tools and documented normalization; WER can exceed 1 and is not a direct safety metric. Separate ASR error from agent failure by testing reference and recognized transcripts. Include language-specific tokenization review. No audio data or ASR adapter is currently supplied.

## Related work and positioning

- [Berkeley Function Calling Leaderboard](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard): tool-calling evaluation.
- [Ticket-Bench](https://arxiv.org/abs/2509.14477): multilingual and regionalized agent evaluation.
- [MASSIVE-Agents](https://aclanthology.org/2025.findings-emnlp.1099/): multilingual agent evaluation derived from MASSIVE.
- [JiWER](https://github.com/jitsi/jiwer): established speech-recognition metrics for a future audio extension.

LocaleSafe does not claim to be the first multilingual agent benchmark. Proposed differentiation is a small, auditable workflow for paired escalation/clarification regressions and traceable tool arguments. Novelty and research significance require a fuller literature review and experiments.

## Deliverables and gates

- v0.1 scaffold: offline evaluator, fixture tests, provenance, documentation.
- v0.2 baseline: reviewed cases, real-agent collection adapter, frozen manifests, baseline technical report, uncertainty estimates, source notebook archive.
- v0.3 / v2 study: preregistered intervention, held-out comparison, ablations, documented negative results.
- Public adoption: external reproduction, reviewed language contributions, and integrations. These are goals, not existing impact claims.
