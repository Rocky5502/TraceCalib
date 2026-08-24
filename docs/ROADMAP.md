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
- success–cost frontier.

## Phase 6 — API robustness subset
- freeze task subset and provider IDs;
- GPT-5.6 Terra, Claude Sonnet 5, DeepSeek V4 Flash, Gemini 3.7 Flash;
- do not enlarge after seeing favorable results.

## Phase 7 — RQ4 AIDev
- eligible sample and annotation codebook;
- validated taxonomy classifier;
- mixed-effects association models;
- forest plot and error analysis.

## Phase 8 — manuscript and artifact
- regenerate every table/figure;
- replace manuscript XX/TBD values only from structured results;
- compile paper;
- prepare release-safe artifact and reproducibility audit.
