# Format follow-up execution history

October 22, 2026, America/New_York.

The collector/protocol were frozen in commit `9860297` before collection. Free Colab GPU allocation initially failed due to usage limits. Allocation later succeeded during the October 22 22:49 UTC follow-up. The uploaded package matched every local source and frozen job-plan byte; its SHA256 was `35afda322c762f4701f75fe54d9d10ba5823c3215bafff7790c28eec70317c27`.

Mistral completed all 128 calls. Its embedded ZIP was captured and verified locally: 137742 bytes, SHA256 `edf24a3319e64fc23ce6f7e17936c22a041c57de3c6e912c18e69b53eb5302f1`. Archive inventory, source/input hashes, schedule, prompts and all recomputed scores passed the offline auditor. Its baseline repeated the original raw output text on all 64 prompts. Raw files are preserved in `experiments/results/format-mistral-7b-v03-20261022`.

The notebook then printed `FORMAT_START phi4-mini`, but the runtime disconnected before any Phi progress or result archive was visible. The reason for disconnection is not established. Reconnection provided a fresh session with only `sample_data`; previous ephemeral Phi files were unavailable. No completed Phi calls from that startup are claimed, and absence of a retained log does not prove no inference occurred.

The unchanged Phi-only schedule was restarted in a new directory during the October 23 00:52 UTC follow-up (October 22 locally). Mistral was not rerun. The restarted Phi run remains pending; this file does not claim the full 256-call follow-up is complete. Both the interrupted startup and recovery remain in separate notebook cells. Original failed development results are unchanged.
