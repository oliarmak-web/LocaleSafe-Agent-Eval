"""Run once in a free T4 notebook after uploading hindi-pair-package.zip."""
import base64
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

from IPython.display import HTML, display

import torch
if not torch.cuda.is_available() or "T4" not in torch.cuda.get_device_name(0):
    raise RuntimeError("Frozen protocol requires a free T4; no runtime substitution")
subprocess.run([sys.executable, "-m", "pip", "install", "transformers==4.57.6",
                "sentencepiece", "protobuf", "accelerate", "--quiet"], check=True)
root = Path("/content/localesafe-hindi-pair-20261027")
root.mkdir(exist_ok=False)
package = Path("/content/hindi-pair-package.zip")
print("HINDI_PACKAGE_SHA256", hashlib.sha256(package.read_bytes()).hexdigest(), flush=True)
with zipfile.ZipFile(package) as archive:
    for name in archive.namelist():
        if not (root / name).resolve().is_relative_to(root.resolve()):
            raise ValueError("Unsafe archive path")
    archive.extractall(root)
os.chdir(root)
proc = subprocess.Popen([sys.executable, "-u", "-m", "localesafe.collect_hindi_pair",
                         "--model", "qwen3-4b", "--split", "development",
                         "--output-dir", "reports/hindi-pair-qwen3-4b"],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
for line in proc.stdout:
    print(line, end="", flush=True)
code = proc.wait()
archive = Path(shutil.make_archive("/content/hindi-pair-qwen3-4b", "zip", root))
data = archive.read_bytes()
display(HTML('<a download="hindi-pair-qwen3-4b.zip" href="data:application/zip;base64,'
             + base64.b64encode(data).decode() + '">Download Hindi pair qwen3-4b</a>'))
print("HINDI_ARCHIVE", len(data), hashlib.sha256(data).hexdigest(), flush=True)
print("HINDI_COLLECTION_FINISHED" if code == 0 else "HINDI_RUNTIME_FAILURE", code, flush=True)
