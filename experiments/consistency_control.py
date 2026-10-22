"""Post-hoc English rerun control; no new model calls or archive mutations."""
import argparse
import json
from pathlib import Path

from experiments.summarize_workflow import audit
from localesafe.evaluate import sha256


def compare(rows, condition):
    selected = [r for r in rows if r["condition"] == condition]
    index = {(r["scenario"], r["language"], r["repeat"]): r for r in selected}
    if len(index) != len(selected):
        raise ValueError("duplicate attempt")
    scenarios = sorted({r["scenario"] for r in selected})
    languages = sorted({r["language"] for r in selected})
    expected = {(s, lang, repeat) for s in scenarios for lang in languages for repeat in (0, 1)}
    if not scenarios or "en" not in languages or set(index) != expected:
        raise ValueError("requires a complete two-repeat language grid")
    anchors = [index[s, "en", repeat] for s in scenarios for repeat in (0, 1)]

    def counts(pairs):
        result = dict(pairs=len(pairs), left_correct=0, both_correct=0,
                      left_only=0, right_only=0, both_wrong=0)
        for left, right in pairs:
            a = left["scores"]["strict"]["correct_action"]
            b = right["scores"]["strict"]["correct_action"]
            result["left_correct"] += int(a)
            result["both_correct" if a and b else "left_only" if a else "right_only" if b else "both_wrong"] += 1
        return result

    result = {"independent_scenarios": len(scenarios),
              "english_rerun": counts([(a, index[a["scenario"], "en", 1-a["repeat"]]) for a in anchors]),
              "same_repeat_target": {}, "other_repeat_target": {}}
    for language in languages:
        if language == "en":
            continue
        for field, flip in (("same_repeat_target", False), ("other_repeat_target", True)):
            result[field][language] = counts([(a, index[a["scenario"], language,
                                                      1-a["repeat"] if flip else a["repeat"]]) for a in anchors])
    return result


def analyze(directories):
    runs = []
    for directory in directories:
        manifest, _, rows = audit(directory)
        if manifest["settings"]["repeats"] != 2:
            raise ValueError("requires exactly two recorded repeats")
        runs.append({"archive": directory.name, "model": manifest["settings"]["model"]["model"],
                     "manifest_sha256": sha256(directory / "manifest.json"),
                     "attempts_sha256": manifest["attempts_sha256"],
                     "conditions": {c: compare(rows, c) for c in ("baseline", "recovery")}})
    return {"analysis": "post-hoc English rerun control", "new_model_calls": 0, "runs": runs}


def render(result):
    lines = ["# Would English also fail on a rerun?", "",
             "Post-hoc analysis of the existing 1,800 decisions. No new model calls. Strict action correctness; invalid outputs remain failures.", "",
             "For every successful English output, compare the other English repeat with the target-language output. The English rerun changes the sampling seed; the request stays exactly the same. Target requests use authored draft translations.", "",
             "| Model / condition | Successful English anchors | Fail on English rerun | Fail in Spanish | Chinese | Ukrainian | Haitian Creole |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    for run in result["runs"]:
        for condition, metrics in run["conditions"].items():
            en = metrics["english_rerun"]
            cells = [str(metrics["same_repeat_target"][lang]["left_only"]) for lang in ("es", "zh-Hans", "uk", "ht")]
            lines.append(f"| {run['model'].split('/')[-1]} / {condition} | {en['left_correct']} | {en['left_only']} | " + " | ".join(cells) + " |")
    lines += ["", "## Plain-English interpretation", "",
              "The larger model's ordinary English requests lost one of eleven successful outputs on an English rerun. Four to nine of those same English successes failed in the matched other-language outputs. In these recorded pairs, cross-language differences were larger than this particular English rerun control. That does not identify their cause.", "",
              "The smaller model's correction setup lost none of its 58 successful English outputs on the other English repeat, while target-language misses ranged from 13 to 56. Its ordinary-request English score was zero, so that condition cannot estimate how well English successes transfer.", "",
              "These observations strengthen the case for investigating language and conversation setup. They do not establish language bias, a stable failure rate or statistical significance.", "",
              "## Limits", "",
              "There are only two repeats per scenario. Both English comparison directions are counted; they are dependent, not extra independent trials. Thirty scenarios come from six templates, and English anchors are reused across language comparisons. Do not pool those comparisons as independent evidence.", "",
              "The cross-language same-repeat pairs share a seed; English reruns use different seeds. Same seeds do not ensure comparable randomness after changing token sequences. The JSON also reports target comparisons using the other repeat as a sensitivity check. Neither pairing removes translation, prompt, model-family or template confounds.", "",
              "Recovery also introduces a JSON example and a scripted rejection. It cannot isolate correction ability. This analysis was chosen after viewing the results; it is exploratory, not a preregistered confirmation. A stronger study needs reviewed meanings, more independent scenarios, more repeats and deterministic-decoding controls.", "",
              "## Reproduce", "", "```sh",
              "python -m experiments.consistency_control experiments/results/workflow-gpu-qwen3-06b-20261022 experiments/results/workflow-gpu-qwen3-17b-20261022 --output-dir reports/consistency-control",
              "```", "",
              "The command audits archive hashes, prompts, scores and the attempt grid before analysis. It writes a new directory and never edits source archives. Machine-readable counts and source hashes: [consistency-control.json](../experiments/analysis/consistency-control.json)."]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directories", nargs="+", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.directories)
    args.output_dir.mkdir(parents=True, exist_ok=False)
    (args.output_dir / "consistency-control.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "CONSISTENCY_CONTROL.md").write_text(render(result), encoding="utf-8")


if __name__ == "__main__":
    main()
