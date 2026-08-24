from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def run(cmd: list[str]) -> str | None:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    except (FileNotFoundError, subprocess.SubprocessError):
        return None
    text = (proc.stdout or proc.stderr).strip()
    return text or None


def gpu_inventory() -> list[dict[str, str]]:
    query = "index,name,memory.total,driver_version,compute_cap"
    output = run(["nvidia-smi", f"--query-gpu={query}", "--format=csv,noheader,nounits"])
    if not output:
        return []
    rows = []
    for line in output.splitlines():
        values = [item.strip() for item in line.split(",")]
        if len(values) >= 5:
            rows.append({"index": values[0], "name": values[1], "memory_mib": values[2], "driver": values[3], "compute_capability": values[4]})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", default="artifacts/machine_manifest.json")
    args = parser.parse_args()

    manifest = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "python": sys.version,
        "cpu": platform.processor(),
        "gpu": gpu_inventory(),
        "tools": {
            name: bool(shutil.which(name))
            for name in ["git", "docker", "nvidia-smi", "wsl", "gh", "hf"]
        },
        "docker_version": run(["docker", "version", "--format", "{{.Server.Version}}"]),
        "wsl_version": run(["wsl", "--version"]),
    }
    try:
        import torch
        manifest["torch"] = {
            "version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "torch_cuda": torch.version.cuda,
            "device_count": torch.cuda.device_count(),
            "devices": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
        }
    except Exception as exc:  # preflight must survive an absent/broken torch install
        manifest["torch"] = {"error": repr(exc)}

    out = Path(args.write)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
