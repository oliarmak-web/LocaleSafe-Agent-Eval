# Execution history

## October 27, 2026 — preparation

Prepared a separate 56-row, 1,680-call exploratory Qwen3-4B extension. Original English/Spanish cases remain identical. Hindi wording is an AI-authored development draft, with no independent review. Source fixtures, protocol and tests were prepared before collection. Free Colab GPU allocation succeeded; model collection has not yet been verified as started. Earlier experiment archives remain unchanged.

## October 27, 2026 — collection launched

Frozen collection source commit: `f16cb96`. Package SHA256: `5b48f6e4ebf807f6068f14fad85eec58700a956cdb98e0e48faf836b7864d71b` (27,252 bytes); the same hash appeared in Colab before model download.

A private Drive copy was created, but connecting it hit Colab's active-session limit. The original sales-archive notebook already had a newly allocated idle GPU. A new collector cell (Cell 1) was appended there without rerunning or replacing earlier experiment outputs. The collector began package setup and Qwen download. The separate notebook copy was not run; no duplicate model job was started. Collection completion and model-call counts are not yet verified. A final private notebook copy and local archive remain required.

Inference was subsequently verified: 88/1,680 responses were recorded and summary generation was progressing normally. This is a partial progress observation, not a completed result. A quiet follow-up was configured to collect, audit and push the completed archive; completion remains pending.

## October 27, 2026 — completed and audited

All 1,680 calls completed with exit code 0. Embedded ZIP: 274,116 bytes; SHA256 `9d660a01d951b923ea46b46cbfceed6110d01b021abb7cf69b3dbbcc7d06ea7b`. The displayed hash matched the local file. Internal inventory/hashes, full cases/design, model settings, source snapshots, job order, prompts, dependent outputs, seeds, token counts and all scores passed the offline audit.

Raw run: `experiments/results/hindi-pair-qwen3-4b-20261027`. Derived results: `experiments/analysis/hindi-pair/summary.json`; human-readable findings and tables: `docs/HINDI_PAIR_FINDINGS.md` and `docs/HINDI_PAIR_RESULTS.md`. The original English screen passed 8/8 in both required conditions. No evaluation was run. A private Drive copy retains the completed embedded archive: https://colab.research.google.com/drive/1UpUzwv6uCburZ6_RvpcuH8gOIOdb8-mU (LocaleSafe Hindi Pair - Completed 2026-10-27.ipynb). Boundary-follow-up output captured at copy time is partial, not a completed boundary archive.

The final combined private notebook copy is https://colab.research.google.com/drive/1rdKhNfmJk2YTWT6YzQBG4ng-i1vIvdbP. A later pinned-tokenizer audit regenerated and matched all 1,680 native prompt hashes. The final findings retain all-profile failures: one unauthorized full-history attempt and eight generated-narrative attempts, all blocked by the trusted guard.
