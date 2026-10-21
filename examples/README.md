# Fixtures

| Directory/files | Purpose |
|---|---|
| `service/` | 11 English/Spanish episodes; explicit US/GB/unspecified locale; consent and handoff controls |
| `cases.jsonl` | Original 18 airport cases across English, Spanish, Ukrainian |
| `synthetic-perfect.jsonl` | Original scorer positive control |
| `synthetic-failures.jsonl` | Three injected airport failures |

Service oracle traces pass 11/11. Faulty traces pass 7/11: blocked unconfirmed submission, wrong date convention, skipped clarification, wrong handoff language.

All traces here are synthetic. Draft translations need independent review. No real service calls or model performance claims. Authored with AI assistance; fixtures use the repository MIT license.

[Service schema](../docs/SERVICE_SCORING.md). Rebuild service controls: `python -m examples.build_service_controls`.
