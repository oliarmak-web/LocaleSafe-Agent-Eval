# Benchmark registry

| Evaluation | Status | Measures |
|---|---|---|
| LocaleSafe service controls v0.2 | Implemented; synthetic English/Spanish traces | Context, clarification, consent, execution, completion |
| LocaleSafe airport pilot v0.1 | Real model run; 108 outputs | Single-turn decisions and proposed calls across nine language configurations |
| Oracle/injected-failure controls | Passing tests | Harness correctness; not model quality |
| [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) | Not run | External function-calling benchmark |
| [MASSIVE-Agents](https://aclanthology.org/2025.findings-emnlp.1099/) | Not run | External multilingual function calling |
| [MLCL](https://arxiv.org/abs/2601.05366) | Related work; not run | Semantic versus execution-convention failures |
| [Ticket-Bench](https://arxiv.org/abs/2509.14477) | Related work; not run | Multilingual localized task workflows |

Our contribution is the service-workflow harness and explicit controls. Multilingual evaluation and semantic/execution decomposition already exist. Novelty and usefulness require further comparison and external validation.

A metric is not a benchmark. Our JSON match is not BFCL accuracy. No broad fairness, hallucination, clinical, or speech score is claimed.

[Score definitions](SERVICE_SCORING.md) · [Research protocol](RESEARCH_PROTOCOL.md)
