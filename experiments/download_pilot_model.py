"""Download the fixed public pilot model, verify weights, avoid remote code."""

import hashlib
import shutil
import urllib.request
from pathlib import Path

from huggingface_hub import snapshot_download

MODEL = "Qwen/Qwen3-0.6B"
REVISION = "c1899de289a04d12100db370d81485cdf75e47ca"
EXPECTED = "f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b"


def main():
    directory = Path("private/qwen3-06b")
    directory.mkdir(parents=True, exist_ok=True)
    temporary = directory / "model.safetensors.partial"
    final = directory / "model.safetensors"
    if not final.exists():
        url = f"https://huggingface.co/{MODEL}/resolve/{REVISION}/model.safetensors"
        digest = hashlib.sha256()
        count = 0
        with urllib.request.urlopen(url, timeout=60) as response, temporary.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
                digest.update(chunk)
                count += len(chunk)
                if count % (100 * 1024 * 1024) == 0:
                    print(f"Downloaded {count // (1024 * 1024)} MiB", flush=True)
        if digest.hexdigest() != EXPECTED:
            raise ValueError("model checksum mismatch; do not load")
        temporary.rename(final)
    else:
        digest = hashlib.sha256()
        with final.open("rb") as existing:
            while chunk := existing.read(1024 * 1024):
                digest.update(chunk)
        if digest.hexdigest() != EXPECTED:
            raise ValueError("existing model checksum mismatch")
    snapshot = Path(snapshot_download(MODEL, revision=REVISION, token=False,
                                     allow_patterns=["*.json", "*.txt", "*.jinja"],
                                     ignore_patterns=["model.safetensors.index.json"]))
    for source in snapshot.iterdir():
        if source.is_file() and source.suffix in {".json", ".txt", ".jinja"}:
            shutil.copyfile(source, directory / source.name)
    print(f"Verified model SHA-256: {EXPECTED}", flush=True)
    print(f"Model available at {directory}", flush=True)


if __name__ == "__main__":
    main()
