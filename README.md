# TraceCalib-SE

**Process-Level Uncertainty Propagation and Selective Control for Reliable Software Engineering Agents**

TraceCalib-SE is a reproducible research framework for studying whether repository-level coding agents can **predict**, **diagnose**, and **control** their own failure risk from stage-wise execution traces. The project is designed around four empirical research questions spanning early failure prediction, uncertainty decomposition, selective intervention, and external validation on real agent-authored pull requests.

> **Status:** experiment infrastructure / protocol freeze. Numerical results are intentionally absent until the frozen analysis pipeline produces them.

## Research questions

**RQ1 — Early failure prediction.** How accurately and how early can stage-wise uncertainty predict final coding-agent failure?

**H1.** Trace-level uncertainty models outperform final verbal confidence, token-likelihood features, self-consistency, and simple trajectory statistics at 25%, 50%, 75%, and 100% of execution.

**RQ2 — Decomposition and transfer.** Which uncertainty components dominate different failure modes, and does decomposition improve transfer?

**H2.** A decomposed model produces better stage attribution and cross-repository calibration than an equally sized scalar-risk model.

**RQ3 — Selective control.** Can uncertainty-specific interventions improve task success under a fixed computational budget?

**H3.** Stage-aware control dominates static retry, final-confidence abstention, test-failure-only repair, and stage-blind conformal control on the success–cost frontier.

**RQ4 — External validation.** Do benchmark-derived uncertainty categories explain human review friction in real agent-authored pull requests?

**H4.** Specification, approach, implementation, testing, and operational uncertainty categories are associated with rejection, revision count, review duration, or human intervention in AIDev pull requests.

## Study design

TraceCalib-SE instruments complete software-agent trajectories and maps each event into one of six actionable stages:

1. specification,
2. retrieval,
3. planning,
4. generation,
5. execution,
6. repair.

The framework then evaluates three capabilities:

- **Predict:** estimate final task failure from partial trajectories.
- **Diagnose:** identify the dominant actionable failure stage.
- **Intervene:** choose a stage-specific action under a fixed budget.

Infrastructure/provider failures are recorded separately and are never relabeled as model uncertainty.

## Primary local models

The initial local matrix uses models already available or practical for the lab workstation:

| Model | Role | Default deployment |
|---|---|---|
| `Qwen/Qwen3-8B` | primary local model | local Transformers/vLLM, pinned revision |
| `mistralai/Mistral-7B-Instruct-v0.3` | primary local model | local Transformers/vLLM, pinned revision |
| `google/gemma-3-12b-it` | larger local robustness model | local multi-GPU/quantized deployment after license acceptance |

Gemma model files require acceptance of Google's Gemma usage terms on Hugging Face before download.

## API reference models

API models are **secondary robustness/reference models**, not replacements for the local primary matrix. Exact IDs and pricing are frozen at experiment time.

- OpenAI: `gpt-5.6-terra`
- Anthropic: `claude-sonnet-5`
- DeepSeek: `deepseek-v4-flash`
- Google: `gemini-3.7-flash`

The API subset is deliberately smaller to control cost and reduce model-version drift.

## Agent scaffolds

The experiment adapters are designed for two complementary agent topologies:

- **mini-SWE-agent** — interactive, linear, trace-friendly execution.
- **Agentless** — localization → repair → validation pipeline.

Upstream repositories are pinned by Git SHA before the pilot. We do not modify upstream projects in place; TraceCalib-SE wraps them through adapters.

## Datasets

### SWE-bench Verified

Primary controlled benchmark for RQ1–RQ3.

- Hugging Face: `princeton-nlp/SWE-bench_Verified`
- 500 verified tasks.
- The repository stores only acquisition code, manifests, hashes, and derived metadata — **not checked-out benchmark repositories or raw Docker environments**.

### AIDev

External validation dataset for RQ4.

- Hugging Face: `hao-li/AIDev`
- Large-scale agent-authored pull-request/review data.
- The repository stores scripts and versioned manifests; raw Parquet files remain outside Git.

Run `python scripts/download_datasets.py --all` after creating the environment.

## Hardware profile

Current lab profile (must be verified by `scripts/preflight.py` before publication):

- Windows 11 workstation
- 64 GB system RAM
- user-reported dual-GPU configuration; exact inventory **TO VERIFY**
- captured device: NVIDIA GeForce RTX 5070 Ti
- captured device memory: 15.92 GiB

The exact GPU count, driver, CUDA runtime, PyTorch build, model quantization, and software versions are written to `artifacts/machine_manifest.json` by preflight and later copied into the manuscript.

## Repository layout

```text
TraceCalib/
├── configs/              # datasets, models, agents, experiment tiers
├── data/                 # README + manifests only; raw data ignored by Git
├── docs/                 # protocol, RQs, model/data notes
├── scripts/              # preflight, downloads, validation, pilot entry points
├── src/tracecalib/       # reusable research code
│   ├── data/
│   ├── instrumentation/
│   ├── providers/
│   └── reporting/
├── tests/                # schema/config/provider tests
├── results/              # generated result artifacts (mostly ignored)
├── AGENTS.md             # Codex/research-engineering rules
├── pyproject.toml
└── .env.example
```

## Quick start

### 1. Windows / WSL2

For the full SWE-bench pipeline, use WSL2 + Docker rather than executing repository containers directly in native Windows paths.

```bash
git clone https://github.com/Rocky5502/TraceCalib.git
cd TraceCalib
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev,ml]'
```

### 2. Preflight

```bash
python scripts/preflight.py --write artifacts/machine_manifest.json
python scripts/validate_config.py
```

### 3. Credentials

Copy the template, but never commit the resulting `.env`:

```bash
cp .env.example .env
```

API/provider credentials are optional until the API reference phase.

### 4. Download data

```bash
python scripts/download_datasets.py --all
```

### 5. Run the pilot

The full study must **not** start until the pilot gate passes.

```bash
python scripts/run_pilot.py --config configs/experiments/pilot.yaml
```

## Evaluation outputs

The reporting contract requires machine-generated versions of:

- run accounting,
- sample characteristics,
- failure prediction,
- early warning,
- condition robustness,
- stage attribution,
- uncertainty decomposition,
- selective control,
- action effectiveness,
- ablations,
- AIDev external validation,
- compute/cost accounting.

Primary metrics include AUROC, AUPRC, Brier score, NLL, ECE/ACE, warning lead time, Macro-F1, risk–coverage, and success–cost utility. Repository-grouped uncertainty intervals and matched-budget comparisons are mandatory.

## Reproducibility rules

- Never fabricate or manually type result values.
- Never use gold patches, future trajectory events, final task labels, or hidden-test outcomes as online features.
- Keep train/calibration/test partitions repository-disjoint.
- Keep paired seeds, perturbations, and interventions for one task in the same partition.
- Separate infrastructure failures from agent failures.
- Pin every dataset, model, provider endpoint, prompt/config, agent scaffold, and container revision.
- Report null and negative findings.
- Do not silently substitute models/providers.
- Do not commit secrets, raw benchmark checkouts, large model weights, or unrestricted raw traces.

## Security note

This repository is currently public. Keep API keys, Hugging Face tokens, local model paths, private traces, and unpublished manuscript data outside Git. `.env`, raw data directories, weights, and execution caches are ignored by default.

## Citation

A citation entry will be added after the manuscript metadata and archival artifact DOI are frozen.

## License

Research code is released under the Apache-2.0 license unless otherwise noted. Third-party models, datasets, and upstream agent repositories retain their original licenses and terms.
