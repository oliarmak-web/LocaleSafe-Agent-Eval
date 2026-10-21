"""Download public, pinned Qwen3-1.7B files without credentials or remote code."""
import json
import urllib.request
from pathlib import Path

from localesafe.evaluate import sha256

MODEL = "Qwen/Qwen3-1.7B"
REVISION = "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e"
WEIGHTS = {
    "model-00001-of-00002.safetensors": "169ad53ec313c3a34b06c0809216e4fc072cce444a5d4ff2b59690d064130ed5",
    "model-00002-of-00002.safetensors": "912becff8d60672aa8628ef08c05898d9adf17c2ad4ae3caf99b065622fdeff9",
}


def main():
    directory = Path("private/qwen3-17b")
    directory.mkdir(parents=True, exist_ok=True)
    names = [*WEIGHTS, "config.json", "generation_config.json", "merges.txt", "model.safetensors.index.json",
             "tokenizer.json", "tokenizer_config.json", "vocab.json", "README.md", "LICENSE"]
    for name in names:
        target = directory / name
        if target.exists() and (name not in WEIGHTS or sha256(target) == WEIGHTS[name]):
            continue
        partial = directory / (name + ".partial")
        with urllib.request.urlopen(f"https://huggingface.co/{MODEL}/resolve/{REVISION}/{name}", timeout=60) as response, partial.open("wb") as output:
            size = 0
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
                size += len(chunk)
                if size % (256 * 1024 * 1024) == 0:
                    print(f"{name}: {size // 1048576} MiB", flush=True)
        if name in WEIGHTS and sha256(partial) != WEIGHTS[name]:
            raise ValueError("weight checksum mismatch")
        partial.replace(target)
        print(f"Verified {name}", flush=True)
    (directory / "provenance.json").write_text(json.dumps({"model": MODEL, "revision": REVISION, "weights": WEIGHTS}, indent=2))


if __name__ == "__main__":
    main()
