# Format follow-up execution history

October 22, 2026, America/New_York.

The collector/protocol were frozen in commit `9860297` before collection. Free Colab GPU allocation initially failed due to usage limits. Allocation later succeeded during the October 22 22:49 UTC follow-up. The uploaded package matched every local source and frozen job-plan byte; its SHA256 was `35afda322c762f4701f75fe54d9d10ba5823c3215bafff7790c28eec70317c27`.

Mistral completed all 128 calls. Its embedded ZIP was captured and verified locally: 137742 bytes, SHA256 `edf24a3319e64fc23ce6f7e17936c22a041c57de3c6e912c18e69b53eb5302f1`. Archive inventory, source/input hashes, schedule, prompts and all recomputed scores passed the offline auditor. Its baseline repeated the original raw output text on all 64 prompts. Raw files are preserved in `experiments/results/format-mistral-7b-v03-20261022`.

The notebook then printed `FORMAT_START phi4-mini`, but the runtime disconnected before any Phi progress or result archive was visible. The reason for disconnection is not established. Reconnection provided a fresh session with only `sample_data`; previous ephemeral Phi files were unavailable. No completed Phi calls from that startup are claimed, and absence of a retained log does not prove no inference occurred.

The unchanged Phi-only schedule was restarted in a new directory during the October 23 00:52 UTC follow-up (October 22 locally). Mistral was not rerun. The restarted Phi run subsequently completed all 128 calls. Both the interrupted startup and recovery remain in separate notebook cells. Original failed development results are unchanged.


The recovered Phi archive was captured and verified: 136961 bytes, SHA256 `3b1137fcd87a9f446b4cca4c4990d3ada575d42cd2381921f2bcfd557d7e1f17`. Both completed runs match the full frozen job plan and pass archive, prompt and score replay checks. The verified follow-up contains 256 retained calls. Each baseline matched its 64 original raw replies exactly. Combined summaries report gains and regressions separately; original results are unchanged. Phi completed around 8:57 PM America/New_York October 22. A TensorFlow startup warning about CUDA does not describe the PyTorch collector: the manifest records the actual Tesla T4 and PyTorch CUDA configuration, and the collector requires CUDA before scheduling inference.
