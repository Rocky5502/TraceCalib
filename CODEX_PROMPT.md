# Codex Start Prompt — TraceCalib-SE

You are the principal research engineer and empirical-SE scientist for this repository. Read `AGENTS.md`, `README.md`, all files in `docs/`, `configs/`, and `data/manifests/` before changing code.

Your goal is to bring TraceCalib-SE from bootstrap to a reproducible local pilot, then only after the pilot gate passes, scale to the full study.

## Scientific requirements

The four RQs are frozen in `docs/RESEARCH_QUESTIONS.md`. The project studies stage-wise uncertainty at specification, retrieval, planning, generation, execution, and repair stages.

You must preserve these invariants:

- no fabricated results;
- no test leakage;
- repository-disjoint train/calibration/test splits;
- infrastructure failures separated from agent failures;
- no silent model/provider substitution;
- all table/figure values generated from machine-readable outputs;
- every result has Git/data/model/agent/protocol provenance;
- report negative/null findings.

## Local workstation

User-reported environment:

- Windows 11;
- 64 GB system RAM;
- user reports two GPUs, but exact inventory must be detected;
- captured GPU: NVIDIA GeForce RTX 5070 Ti;
- captured device memory: 15.92 GiB.

Run `python scripts/preflight.py --write artifacts/machine_manifest.json` and trust the detected values over prose. Do not assume two GPUs aggregate memory unless the serving backend actually supports model parallelism.

## Local primary models

1. `Qwen/Qwen3-8B` — already present locally according to the owner.
2. `mistralai/Mistral-7B-Instruct-v0.3` — already present locally according to the owner.
3. `google/gemma-3-12b-it` — add only after license access and VRAM/quantization validation.

Run `python scripts/check_local_models.py` and discover actual local revisions/paths. Pin exact revisions before pilot execution.

## API robustness/reference models

Do not run these over the entire matrix by default. Use a frozen secondary subset after the local pilot and budget review:

- OpenAI `gpt-5.6-terra`;
- Anthropic `claude-sonnet-5`;
- DeepSeek `deepseek-v4-flash`;
- Google `gemini-3.7-flash`.

Use provider adapters with retries, request IDs, usage/cost capture, and no silent fallback.

## Datasets

- RQ1–RQ3: `princeton-nlp/SWE-bench_Verified`, bootstrap pin `c104f84`.
- RQ4: `hao-li/AIDev`, bootstrap pin `68ed5f4`.

Run `python scripts/download_datasets.py --all`. Raw data, repository checkouts, model weights, and Docker caches stay outside Git. Record hashes/manifests.

## Agent scaffolds

- mini-SWE-agent;
- Agentless.

Pin exact upstream Git SHAs. Do not patch upstream repositories directly; implement adapters under `src/tracecalib/`.

## Immediate implementation order

1. clone/install inside WSL2 Linux filesystem;
2. run preflight, config validation, local-model discovery, and dataset acquisition;
3. pin upstream agent revisions and validate SWE-bench gold-patch Docker execution;
4. implement normalized run/event persistence using `TraceEvent` and `RunRecord`;
5. implement mini-SWE-agent adapter and deterministic stage mapping;
6. implement Agentless adapter and deterministic stage mapping;
7. add local OpenAI-compatible serving launchers/configs for Qwen and Mistral;
8. validate Gemma deployment only if stable;
9. implement run-status taxonomy, token/tool/test/runtime/cost accounting, secret redaction, and immutable raw traces;
10. construct a 12-task pilot across >=3 repositories and all practical local model-agent pairs;
11. include clean, ambiguity, and retrieval-degradation conditions;
12. generate one real result table and one real figure from pilot outputs;
13. write `reports/PILOT_REPORT.md` and `reports/SCALE_UP_DECISION.md`;
14. stop before the full matrix unless the gate passes.

## Pilot gate

GO only when:

- SWE-bench gold-patch validation works;
- both agent adapters produce reconstructable schema-valid traces;
- exact local model revisions/deployments are pinned;
- infrastructure failure rate <=15%;
- no secrets appear in logs;
- repository-disjoint study split is feasible;
- stressors remain natural/solvable;
- projected API/storage/compute budget is acceptable;
- result-table and figure generation is fully scripted.

## Full-study planning note

The new primary local matrix is 3 local models × 2 agent scaffolds. This expands the earlier two-model manuscript design. Do not freeze the full requested-run count until the pilot measures cost/throughput and a power/precision analysis confirms the sample plan. Record any manuscript-impacting change as a protocol amendment rather than silently changing the paper.

Begin by inspecting the repository, creating `reports/PRE_FLIGHT_REPORT.md`, and implementing the missing benchmark/agent adapters. Do not only describe what you plan to do—make the code changes, test them, commit coherent units, and keep `STATUS.md` current.
