# Execution history

October 27, 2026: protocol, domain policies and all 180 draft cases prepared before collection. 720 greedy calls planned; no completed model results yet. Text checkpoints only; independent language/domain review is outstanding.

## Startup and recovery

Frozen source commit `bda0e3a`. Package 38,697 bytes; SHA256 `4333246d63762619f3f6213784f6fc95b593b47e8b7a18bdd6f80b5014c0b428`.

The old runtime had disconnected after inactivity. A free T4 was allocated without paying or changing accounts. Initial Cell 4 startup failed before invoking the model collector because /content/domain-study-package.zip was absent. Two file-chooser upload attempts did not produce a visible runtime file. The original failed cell and empty initial directory were retained.

Recovery Cell 5 transferred the exact ZIP bytes through the code editor, asserted their SHA256 and used a new root /content/localesafe-domain-study-recovery1-20261027. Only package delivery and the runtime directory changed; frozen cases, instructions, scoring and model settings did not. The same package hash appeared before model download. Inference was verified at 24/720 calls. No duplicate or replacement model generations were recorded before recovery. Completion remains pending.

## Qwen completed; Phi replication started

Qwen completed all 720 requests with exit code 0. ZIP 233,972 bytes; SHA256 `8cc862ad24838a1848998afb9abfd84eeb08b63fe461c0ca938fa73217c7898d` matched locally. Internal inventory/hashes, frozen cases/design, source snapshots, prompts, dependencies, settings, seeds, scores and token limits passed audit. Raw archive: `experiments/results/domain-study-qwen3-4b-20261027`; derived summary: `experiments/analysis/domain-study/qwen.json`.

English full-history/reference screens: security 5/6 and 5/6; finance 5/6 and 5/6; healthcare administration 5/6 and 5/6; insurance 4/6 and 5/6 (FAILED); telecom 5/6 and 6/6. Insurance cannot support a strong language interpretation.

Phi replication frozen in commit `441656e`. Package 40,168 bytes; SHA256 `66108408c57f72e91fd6dd4cc6f8a05f0e085bd53cb222766f488cab2b32a94c`. Started in Cell 6 after the Qwen archive passed audit. Exact package bytes were transferred via the editor with a hash assertion, avoiding the failed file-chooser path. No simultaneous model processes or prompt changes. Phi completion remains pending.
