from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import snapshot_download

from tracecalib.config import load_yaml


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(name: str, spec: dict, root: Path) -> dict:
    target = root / name
    local = Path(
        snapshot_download(
            repo_id=spec["repo_id"],
            repo_type=spec.get("repo_type", "dataset"),
            revision=spec["revision"],
            allow_patterns=spec.get("allow_patterns"),
            local_dir=target,
        )
    )
    files = []
    for path in sorted(local.rglob("*")):
        if path.is_file() and ".cache" not in path.parts:
            files.append({"path": str(path.relative_to(local)), "bytes": path.stat().st_size, "sha256": sha256(path)})
    known = spec.get("known_file_sha256", {})
    mismatches = []
    by_path = {row["path"]: row["sha256"] for row in files}
    for rel, expected in known.items():
        if by_path.get(rel) != expected:
            mismatches.append({"path": rel, "expected": expected, "actual": by_path.get(rel)})
    if mismatches:
        raise RuntimeError(f"Checksum mismatch for {name}: {mismatches}")
    return {
        "name": name,
        "repo_id": spec["repo_id"],
        "revision": spec["revision"],
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": files,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--dataset", action="append", default=[])
    parser.add_argument("--root", default="data/raw")
    args = parser.parse_args()

    config = load_yaml("configs/datasets.yaml")["datasets"]
    names = list(config) if args.all else args.dataset
    if not names:
        parser.error("Choose --all or at least one --dataset NAME")

    root = Path(args.root)
    root.mkdir(parents=True, exist_ok=True)
    manifests = Path("data/manifests/downloaded")
    manifests.mkdir(parents=True, exist_ok=True)

    for name in names:
        if name not in config:
            raise KeyError(f"Unknown dataset: {name}")
        manifest = download(name, config[name], root)
        out = manifests / f"{name}.json"
        out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"Downloaded {name}; manifest -> {out}")


if __name__ == "__main__":
    main()
