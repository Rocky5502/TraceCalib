# Dataset Registry

## SWE-bench Verified — RQ1/RQ2/RQ3

Repository: `princeton-nlp/SWE-bench_Verified`

Pinned bootstrap revision: `c104f84`.

The current Verified dataset contains 500 tasks. The parquet file is small, but task execution requires cloning repositories and building/running benchmark environments. Those checkouts and Docker layers belong in local caches, not Git.

The loader records SHA256 hashes after download and compares the known Verified parquet hash when available.

## AIDev — RQ4

Repository: `hao-li/AIDev`

Pinned bootstrap revision: `68ed5f4`.

AIDev is large enough that raw parquet files should stay outside Git. The downloader initially acquires only PR/repository/review/comment tables needed by RQ4. The exact eligible sample, filters, deduplication, and annotation subset are frozen in later manifests.

## Why raw datasets are not committed

1. provenance is stronger when acquisition is scripted and revision-pinned;
2. AIDev is large and changes over time;
3. SWE-bench execution creates large repository and Docker caches;
4. public Git should not become a storage mechanism for third-party data;
5. derived traces may contain repository content or provider outputs requiring review before release.

Commit only dataset manifests, hashes, selection IDs, splits, annotations permitted for release, and derived statistics.
