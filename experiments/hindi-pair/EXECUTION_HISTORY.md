# Execution history

## October 27, 2026 — preparation

Prepared a separate 56-row, 1,680-call exploratory Qwen3-4B extension. Original English/Spanish cases remain identical. Hindi wording is an AI-authored development draft, with no independent review. Source fixtures, protocol and tests were prepared before collection. Free Colab GPU allocation succeeded; model collection has not yet been verified as started. Earlier experiment archives remain unchanged.

## October 27, 2026 — collection launched

Frozen collection source commit: `f16cb96`. Package SHA256: `5b48f6e4ebf807f6068f14fad85eec58700a956cdb98e0e48faf836b7864d71b` (27,252 bytes); the same hash appeared in Colab before model download.

A private Drive copy was created, but connecting it hit Colab's active-session limit. The original sales-archive notebook already had a newly allocated idle GPU. A new collector cell (Cell 1) was appended there without rerunning or replacing earlier experiment outputs. The collector began package setup and Qwen download. The separate notebook copy was not run; no duplicate model job was started. Collection completion and model-call counts are not yet verified. A final private notebook copy and local archive remain required.
