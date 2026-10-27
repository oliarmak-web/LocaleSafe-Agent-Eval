# Execution history

October 27, 2026: frozen after inspecting Hindi-pair errors, before operation-probe collection. 336 greedy calls planned; none verified yet. No new reference labels or prompt changes after results are permitted.

Source frozen in commit `ea2117a`. Package 28,553 bytes; SHA256 `905c61afa74ad6d3329f7da1d2e0af77c3b24ca4063333d9e6b5830abe37f65c`. Launched in Cell 3 of the runtime notebook after the 864-call boundary job completed, with no overlapping model process. Progress verified at 304/336; archive collection/audit remain pending.

## Completed and audited

All 336 calls completed with exit code 0. ZIP 131,916 bytes; SHA256 `5c2eed7bd4f9c8626bea86d650cb24b231d23b46458793d8b0b692a4da2db406` matched locally. Package hash matched the displayed Colab value. Archive inventory/hashes, sources, frozen cases/jobs, settings, messages, scores and output-token limits passed audit. Parent Hindi-pair archive was independently audited during analysis. Results are in `experiments/results/operation-probe-qwen3-4b-20261027` and `experiments/analysis/operation-probe/summary.json`.

All 336 replies were valid letters; none selected A. Every case changed correctness across option orders, including English. The probe does not establish a language ranking or repair the original agent.

All three completed studies were saved in a private Drive copy: https://colab.research.google.com/drive/1rdKhNfmJk2YTWT6YzQBG4ng-i1vIvdbP (LocaleSafe Language Diagnostics - Completed 2026-10-27.ipynb). The copied notebook visibly retained all three archive hashes and exit-code-0 completion markers. Sharing was not changed.

A separate local audit downloaded only public tokenizer/config files at the pinned Qwen revision, not model weights, and regenerated the native chat-template strings. All 2,880 recorded prompt hashes matched: Hindi pair 1,680; boundary 864; operation probe 336. The first offline cache lookup found no tokenizer; a subsequent default-cache download hit Windows symlink permissions. Downloading to an ignored local artifact directory succeeded without permission changes. These were analysis-tool setup issues, not failed or replacement model generations.
