# Output-contract prompt control

Specified October 22, 2026, after viewing Mistral/Phi development failures and before collecting this follow-up. This is exploratory, with no held-out or first-discovery claim.

Question: does removing tool-name prefixes from the JSON examples improve strict action correctness while preserving task information?

Use the 32 archived development cases for each of Mistral-7B-Instruct-v0.3 and Phi-4-mini-instruct. For each case, test full history and the authored reference record. Compare an exact original-prompt repeat with a prompt replacing only `Tools: wait {...}; propose {...}; commit {...}` with JSON-only example objects. The replacement is frozen in `build_format_followup.py`; all task evidence, tool names inside objects, fields and policies remain unchanged. This is a prompt intervention, not constrained decoding or output repair. Correctness still requires exact valid JSON and the expected action. Interpretation of meaning separately from formatting remains limited.

64 parent actor prompts per model × two arms = 128 calls per model, 256 total. Greedy generation, max 96 new tokens, pinned weights and native templates, Transformers 4.57.6, float16, no quantization. Batch size 1 for Mistral, 8 for Phi; independent deterministic shuffled schedules with seed 20261024. Record all raw outputs, token counts, prompts, scores, runtime and source hashes. Use only free GPU resources. Model baselines may change numerically with runtime/batch changes; report baseline-repeat agreement rather than assuming it.

Primary outcomes: valid action JSON and exact correct action, paired by model, case and evidence condition. Secondary: unauthorized valid commits, guard blocks and token-limit hits. Report language cells descriptively; repeated cases and eight development variants do not support a language ranking or significance claim. Do not rerun evaluation under changed prompts or replace original failed results. Any later evaluation needs a separately frozen protocol and new cases.

Preserve incomplete attempts on runtime failure. Recompute every score, verify the archived job plan and hashes, and report both gains and regressions. This study diagnoses a prerequisite for future order-change experiments; it does not implement live orders or measure production failure prevalence.
