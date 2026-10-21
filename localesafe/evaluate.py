"""Strict artifact validation and deterministic behavioral scoring."""

import hashlib
import json
from collections import defaultdict
from pathlib import Path


def read_jsonl(path):
    rows = []
    for line_no, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON") from exc
    if not rows:
        raise ValueError(f"{path}: empty artifact")
    return rows


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _calls(value):
    _require(isinstance(value, list), "tool_calls must be a list")
    for call in value:
        _require(isinstance(call, dict) and set(call) == {"name", "arguments"}, "invalid tool call fields")
        _require(isinstance(call["name"], str) and bool(call["name"]), "invalid tool name")
        _require(isinstance(call["arguments"], dict), "arguments must be an object")
    return sorted(json.dumps(c, sort_keys=True, ensure_ascii=False, allow_nan=False) for c in value)


def validate(cases, responses):
    _require(isinstance(cases, list) and bool(cases), "cases must be a nonempty list")
    _require(isinstance(responses, list), "responses must be a list")
    ids = set()
    pairs = defaultdict(list)
    for case in cases:
        _require(isinstance(case, dict), "case must be an object")
        _require(set(case) == {"id", "pair_id", "language", "split", "text", "translation_status", "expected"}, "invalid case fields")
        for key in ("id", "pair_id", "language", "text"):
            _require(isinstance(case[key], str) and bool(case[key]), f"invalid {key}")
        _require(case["id"] not in ids, "duplicate case id")
        ids.add(case["id"])
        _require(case["split"] in {"dev", "test"}, "invalid split")
        _require(case["translation_status"] in {"draft", "reviewed", "source"}, "invalid translation status")
        expected = case["expected"]
        _require(isinstance(expected, dict) and set(expected) == {"decision", "tool_calls"}, "invalid expected fields")
        _require(expected["decision"] in {"escalate", "clarify", "respond"}, "invalid expected decision")
        _calls(expected["tool_calls"])
        pairs[case["pair_id"]].append(case)
    for group in pairs.values():
        _require(len({c["language"] for c in group}) == len(group), "duplicate language in pair")
        _require(len({c["split"] for c in group}) == 1, "pair leaks across splits")
        _require(len({json.dumps(c["expected"], sort_keys=True) for c in group}) == 1, "paired expectations differ")
        _require(any(c["language"] == "en" for c in group), "pair requires English reference")
    seen = set()
    for response in responses:
        _require(isinstance(response, dict) and set(response) == {"id", "decision", "tool_calls"}, "invalid response fields")
        _require(isinstance(response["id"], str) and response["id"] in ids, "unknown response id")
        _require(response["id"] not in seen, "duplicate response id")
        seen.add(response["id"])
        _require(response["decision"] in {"escalate", "clarify", "respond"}, "invalid response decision")
        _calls(response["tool_calls"])
    _require(seen == ids, "missing responses: all cases must be represented")


def evaluate(cases, responses):
    validate(cases, responses)
    indexed = {r["id"]: r for r in responses}
    results = []
    for case in cases:
        actual, expected = indexed[case["id"]], case["expected"]
        decision_ok = actual["decision"] == expected["decision"]
        tools_ok = _calls(actual["tool_calls"]) == _calls(expected["tool_calls"])
        results.append({"id": case["id"], "pair_id": case["pair_id"], "language": case["language"],
                        "decision_correct": decision_ok, "tools_exact": tools_ok, "passed": decision_ok and tools_ok,
                        "missed_escalation": expected["decision"] == "escalate" and actual["decision"] != "escalate",
                        "unnecessary_escalation": expected["decision"] != "escalate" and actual["decision"] == "escalate"})
    languages = {}
    for language in sorted({c["language"] for c in cases}):
        subset = [r for r in results if r["language"] == language]
        languages[language] = {"n": len(subset), "pass_rate": sum(r["passed"] for r in subset) / len(subset),
                               "missed_escalations": sum(r["missed_escalation"] for r in subset),
                               "unnecessary_escalations": sum(r["unnecessary_escalation"] for r in subset)}
    paired = {}
    for language in languages:
        if language == "en":
            continue
        gaps = []
        for result in results:
            if result["language"] == language:
                reference = next(r for r in results if r["pair_id"] == result["pair_id"] and r["language"] == "en")
                gaps.append(int(reference["passed"]) - int(result["passed"]))
        paired[language] = {"n_pairs": len(gaps), "english_minus_language_pass_rate": sum(gaps) / len(gaps)}
    return {"schema_version": 1, "n": len(results), "languages": languages, "paired_gaps": paired,
            "translation_warning": any(c["translation_status"] == "draft" for c in cases), "cases": results}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
