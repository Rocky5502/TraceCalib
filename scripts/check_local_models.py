from __future__ import annotations

import json
import os
from pathlib import Path

from huggingface_hub import scan_cache_dir


TARGETS = {
    "Qwen/Qwen3-8B": os.getenv("LOCAL_QWEN_PATH"),
    "mistralai/Mistral-7B-Instruct-v0.3": os.getenv("LOCAL_MISTRAL_PATH"),
    "google/gemma-3-12b-it": os.getenv("LOCAL_GEMMA_PATH"),
}


def main() -> None:
    found: dict[str, dict] = {model: {"explicit_path": path, "exists": bool(path and Path(path).exists())} for model, path in TARGETS.items()}
    try:
        cache = scan_cache_dir()
        repos = {repo.repo_id: repo for repo in cache.repos if repo.repo_type == "model"}
        for model in TARGETS:
            repo = repos.get(model)
            found[model]["hf_cache"] = bool(repo)
            if repo:
                found[model]["revisions"] = sorted(rev.commit_hash for rev in repo.revisions)
                found[model]["size_on_disk"] = repo.size_on_disk
    except Exception as exc:
        found["_cache_scan_error"] = {"error": repr(exc)}
    print(json.dumps(found, indent=2))


if __name__ == "__main__":
    main()
