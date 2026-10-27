"""Use the unchanged handoff collector with a separately frozen Hindi extension."""
import sys
from . import collect_handoff as collector

EXTRA_SOURCES = ("localesafe/collect_hindi_pair.py", "experiments/build_hindi_pair.py",
                 "experiments/hindi-pair/PROTOCOL.md")


def main():
    if "--cases" in sys.argv or "--design" in sys.argv:
        raise ValueError("Hindi pair uses the frozen extension cases and design")
    if "--model" not in sys.argv or sys.argv[sys.argv.index("--model")+1] != "qwen3-4b":
        raise ValueError("Frozen first run uses qwen3-4b only")
    collector.SOURCES = (*collector.SOURCES, *EXTRA_SOURCES)
    sys.argv += ["--cases", "experiments/hindi-pair/cases.jsonl", "--design", "experiments/hindi-pair/design.json"]
    collector.main()


if __name__ == "__main__":
    main()
