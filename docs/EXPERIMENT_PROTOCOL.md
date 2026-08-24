# Experiment Protocol

## 1. Goal
Evaluate whether stage-wise trace uncertainty provides actionable reliability information beyond endpoint confidence in repository-level coding agents, and whether that value transfers across repositories, model families, and access regimes.

## 2. Primary controlled benchmark
SWE-bench Verified. Select 100 tasks only after repository-level feasibility checks and a power/precision simulation. The final split must be repository-disjoint.

## 3. Agent-model matrix
Primary local study: mini-SWE-agent and Agentless crossed with Qwen3-8B, Mistral-7B-Instruct-v0.3, and Gemma-3-12B-IT.

API models are a secondary robustness/portability subset and are not automatically run over the full matrix.

## 4. Trace stages
- specification
- retrieval
- planning
- generation
- execution
- repair

Each event receives a stage, event type, timestamp, run ID, step ID, normalized progress, tool/model metadata, token/cost accounting, and safe references to prompts/observations.

## 5. Stress conditions
### Ambiguous specification
Remove or blur one acceptance criterion, example, API/entity reference, or disambiguating detail while preserving solvability. Human validation is required.

### Retrieval degradation
Reduce search budget/top-k, omit one initially relevant candidate, inject irrelevant candidates, or add stale/misleading documentation. Never reveal gold changed files to the online agent.

### Repeated seeds
Repeat a frozen subset with two additional seeds while holding all other configuration constant.

## 6. Online-feature leakage policy
Forbidden online features include gold patch content, gold changed-file sets, hidden-test outcomes, final resolution labels, future trajectory events, and post-intervention outcomes.

## 7. Baselines
RQ1/RQ2: verbal confidence, likelihood/entropy, self-consistency, simple trajectory statistics, behavior-only risk, matched-parameter scalar temporal risk, stage model without propagation, and full TraceCalib-SE.

RQ3: always continue, fixed retry, test-failure repair, final-confidence abstention, stage-blind conformal control, random matched-budget intervention, matched more-compute policy, TraceCalib-SE, and oracle stage controller as non-deployable headroom.

RQ5: endpoint confidence, within-model self-consistency, the common black-box stage-wise representation, and white-box-only extensions reported separately. The primary portability test uses leave-one-model-family-out training/calibration with no target-family retuning.

## 8. Statistics
Use repository-grouped bootstrap intervals, paired comparisons for matched policies, Holm correction for planned multiple comparisons, effect sizes, and explicit sensitivity analyses. Keep seeds/perturbations/reruns correlated by original task.

RQ5 reports AUROC retention, ECE degradation, success-cost-area change, and a prespecified non-inferiority/transfer criterion frozen before sealed evaluation.

## 9. Pilot gate
No full study before a local pilot verifies:
- SWE-bench gold-patch Docker evaluation;
- both agent adapters;
- trace schema validity;
- local model stability;
- infrastructure failure rate <= 15%;
- secret-free logs;
- cost/storage feasibility;
- one table and one figure generated end-to-end.

## 10. RQ5 portability tier
After the local pilot passes, freeze leave-one-model-family-out folds over Qwen3-8B, Mistral-7B-Instruct-v0.3, and Gemma-3-12B-IT. Fit risk models and calibrators without the target model family, evaluate the target with the common black-box feature contract, and do not retune on target outcomes.

Only after the portability protocol and budget are frozen, select the API subset from GPT-5.6 Terra, Claude Sonnet 5, DeepSeek V4 Flash, and Gemini 3.7 Flash. Freeze exact provider model strings, reasoning modes, access dates, request settings, and pricing snapshots before execution. Provider ranking is outside scope.
