# AGENTS.md — TraceCalib-SE

## Mission
Build a reproducible empirical artifact for TraceCalib-SE. The repository instruments coding-agent trajectories, estimates stage-wise operational uncertainty, predicts failures, diagnoses failure stages, evaluates matched-budget interventions, analyzes AIDev, tests model-family/access-regime portability, and generates every manuscript result from code.

## Non-negotiable research rules
1. Never fabricate, interpolate, or manually type results.
2. Never use test outcomes for feature design, model selection, threshold tuning, prompt tuning, or cost-vector selection.
3. Use repository-disjoint train/calibration/test partitions. Seeds, perturbations, and paired reruns from one task stay in one partition.
4. Separate agent failures from infrastructure/provider failures.
5. Gold patches, hidden tests, future events, final labels, and post-intervention outcomes are offline/oracle-only and must never become online features.
6. Do not silently substitute models, providers, checkpoints, or agent scaffolds.
7. Pin exact dataset revisions, model revisions, Git SHAs, prompts/configs, and container digests before the scaled run.
8. Report null, negative, and adverse results.
9. Every result table and figure must be generated from machine-readable outputs with provenance.
10. This repository is public: never commit tokens, `.env` files, private raw traces, model weights, or unpublished sensitive artifacts.
11. RQ5 target-model folds must not use target-family outcomes for fitting, calibration, feature selection, or threshold tuning.
12. API portability is not a provider leaderboard; unexecuted API cells remain `N/A`.

## Scientific scope
- RQ1: early failure prediction at 25/50/75/100% execution.
- RQ2: stage-wise decomposition and cross-repository transfer.
- RQ3: matched-budget selective control.
- RQ4: external validation on AIDev pull requests.
- RQ5: leave-one-model-family-out and local-to-API portability under a common black-box feature contract.

## Core local models
- Qwen/Qwen3-8B
- mistralai/Mistral-7B-Instruct-v0.3
- google/gemma-3-12b-it

## Secondary API reference models
- OpenAI gpt-5.6-terra
- Anthropic claude-sonnet-5
- DeepSeek deepseek-v4-flash
- Google gemini-3.7-flash

API models are a robustness/portability subset unless a protocol amendment explicitly changes that role.

## Hardware
User-reported Windows 11 workstation, 64 GB RAM, dual-GPU configuration; captured device is an NVIDIA GeForce RTX 5070 Ti with 15.92 GiB device memory. Treat GPU count and exact inventory as TO VERIFY until `scripts/preflight.py` records it.

## Required execution order
1. preflight and environment manifest;
2. pin upstream agents/models/datasets;
3. validate SWE-bench Docker evaluation;
4. implement trace adapters and schemas;
5. run the pilot;
6. write a scale-up decision;
7. freeze protocol/splits/configs including RQ5 target-family folds;
8. execute the full local matrix;
9. train/calibrate/evaluate RQ1/RQ2 models;
10. run paired RQ3 interventions;
11. execute RQ5 local leave-one-family-out portability;
12. run the frozen API portability subset;
13. execute AIDev/RQ4 validation;
14. generate tables/figures and update the manuscript.

Do not launch the full experiment matrix before the pilot passes.
