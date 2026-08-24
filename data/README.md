# Data Directory

This directory intentionally does **not** contain raw SWE-bench repositories, model weights, Docker caches, or raw AIDev parquet files.

Tracked content:
- `manifests/` — dataset revisions, hashes, selection/split metadata;
- small annotation templates/codebooks;
- release-safe derived metadata.

Ignored local content:
- `raw/`
- `cache/`
- `repos/`
- `docker/`
- `traces/raw/`
- `aidev/raw/`

Acquire the pinned bootstrap datasets with:

```bash
python scripts/download_datasets.py --all
```

Every later frozen dataset/split must have a manifest containing the source revision, SHA256 hashes, generation commit, timestamp, and exclusion reasons.
