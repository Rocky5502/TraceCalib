# Implementation Roadmap

## Phase 0 — machine and repository preflight
- verify exact GPU inventory, VRAM, driver, CUDA/PyTorch and WSL2/Docker;
- discover existing Qwen/Mistral local checkpoints;
- accept/fetch Gemma only if needed;
- pin agent Git SHAs and dataset/model revisions;
- estimate disk/API budget.

## Phase 1 — benchmark and adapters
- validate SWE-bench gold-patch execution;
- implement mini-SWE-agent trace adapter;
- implement Agentless trace adapter;
- normalize both into TraceEvent/RunRecord schemas;
- add infrastructure failure taxonomy.

## Phase 2 — local pilot
- 12 tasks, >=3 repositories;
- both agent scaffolds;
- all practical local models;
- clean + ambiguity + retrieval stress;
- generate one real table and figure;
- produce GO / GO WITH AMENDMENT / NO-GO.

## Phase 3 — protocol freeze and full local matrix
- repository-disjoint splits;
- 3 local models x 2 agents;
- clean, stress, repeated-seed, and intervention runs;
- freeze RQ5 leave-one-model-family-out folds and non-inferiority criterion;
- immutable raw traces and run accounting.

## Phase 4 — uncertainty models and RQ1/RQ2
- feature extraction;
- human stage annotations;
- scalar and decomposed temporal controls;
- calibration;
- sealed test evaluation.

## Phase 5 — RQ3
- paired intervention reruns;
- static, random, more-compute, conformal and oracle controls;
- success-cost frontier.

## Phase 6 — RQ5 local model portability
- common black-box stage-wise feature contract;
- leave Qwen3-8B out, fit/calibrate on the other families, then evaluate Qwen3-8B;
- repeat for Mistral-7B-Instruct-v0.3 and Gemma-3-12B-IT;
- report AUROC retention, ECE degradation, and success-cost-area change;
- run cross-model-disagreement and white-box feature ablations separately;
- never retune on held-out-model outcomes.

## Phase 7 — frozen API portability subset
- freeze task subset, endpoint IDs, reasoning modes, access dates, pricing and budget;
- candidate endpoints: GPT-5.6 Terra, Claude Sonnet 5, DeepSeek V4 Flash, Gemini 3.7 Flash;
- apply the same black-box feature contract;
- report unexecuted endpoints as N/A;
- do not enlarge the subset after seeing favorable results and do not frame it as a leaderboard.

## Phase 8 — RQ4 AIDev
- eligible sample and annotation codebook;
- validated taxonomy classifier;
- mixed-effects association models;
- forest plot and error analysis.

## Phase 9 — manuscript and artifact
- regenerate every table/figure including RQ5;
- replace manuscript XX/TBD values only from structured results;
- compile paper;
- prepare release-safe artifact and reproducibility audit.
