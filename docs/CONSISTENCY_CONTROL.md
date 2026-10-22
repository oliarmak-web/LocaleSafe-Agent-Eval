# Would English also fail on a rerun?

Post-hoc analysis of the existing 1,800 decisions. No new model calls. Strict action correctness; invalid outputs remain failures.

For every successful English output, compare the other English repeat with the target-language output. The English rerun changes the sampling seed; the request stays exactly the same. Target requests use authored draft translations.

| Model / condition | Successful English anchors | Fail on English rerun | Fail in Spanish | Chinese | Ukrainian | Haitian Creole |
|---|---:|---:|---:|---:|---:|---:|
| Qwen3-0.6B / baseline | 0 | 0 | 0 | 0 | 0 | 0 |
| Qwen3-0.6B / recovery | 58 | 0 | 13 | 15 | 19 | 56 |
| Qwen3-1.7B / baseline | 11 | 1 | 4 | 7 | 6 | 9 |
| Qwen3-1.7B / recovery | 10 | 0 | 8 | 0 | 0 | 0 |

## Plain-English interpretation

The larger model's ordinary English requests lost one of eleven successful outputs on an English rerun. Four to nine of those same English successes failed in the matched other-language outputs. In these recorded pairs, cross-language differences were larger than this particular English rerun control. That does not identify their cause.

The smaller model's correction setup lost none of its 58 successful English outputs on the other English repeat, while target-language misses ranged from 13 to 56. Its ordinary-request English score was zero, so that condition cannot estimate how well English successes transfer.

These observations strengthen the case for investigating language and conversation setup. They do not establish language bias, a stable failure rate or statistical significance.

## Limits

There are only two repeats per scenario. Both English comparison directions are counted; they are dependent, not extra independent trials. Thirty scenarios come from six templates, and English anchors are reused across language comparisons. Do not pool those comparisons as independent evidence.

The cross-language same-repeat pairs share a seed; English reruns use different seeds. Same seeds do not ensure comparable randomness after changing token sequences. The JSON also reports target comparisons using the other repeat as a sensitivity check. Neither pairing removes translation, prompt, model-family or template confounds.

Recovery also introduces a JSON example and a scripted rejection. It cannot isolate correction ability. This analysis was chosen after viewing the results; it is exploratory, not a preregistered confirmation. A stronger study needs reviewed meanings, more independent scenarios, more repeats and deterministic-decoding controls.

## Reproduce

```sh
python -m experiments.consistency_control experiments/results/workflow-gpu-qwen3-06b-20261022 experiments/results/workflow-gpu-qwen3-17b-20261022 --output-dir reports/consistency-control
```

The command audits archive hashes, prompts, scores and the attempt grid before analysis. It writes a new directory and never edits source archives. Machine-readable counts and source hashes: [consistency-control.json](../experiments/analysis/consistency-control.json).
