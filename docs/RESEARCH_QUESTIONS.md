# Research Questions and Hypotheses

## RQ1 — Failure prediction and early warning
**How accurately and how early can stage-wise uncertainty predict final coding-agent failure?**

**H1:** Trace-level uncertainty models outperform final verbal confidence, token-likelihood features, self-consistency, and simple trajectory statistics at 25%, 50%, 75%, and 100% of execution.

Primary metrics: AUROC and Brier score at 50% trajectory progress.

Secondary metrics: AUPRC, NLL, ECE, ACE, alert precision, warning lead time, and class-conditional calibration.

## RQ2 — Decomposition and transfer
**Which uncertainty components dominate different failure modes, and does decomposition improve transfer?**

**H2:** A decomposed model produces better stage attribution and cross-repository calibration than an equally sized scalar-risk model.

Primary metric: OOD stage-attribution Macro-F1.

Stages: specification, retrieval, planning, generation, execution, repair.

## RQ3 — Selective control
**Can uncertainty-specific interventions improve task success under a fixed computational budget?**

**H3:** Stage-aware control dominates static retry, final-confidence abstention, test-failure-only repair, and stage-blind conformal control on the success–cost frontier.

Primary metric: area under the success–cost frontier.

The comparison must include a random matched-budget policy and a stage-blind more-compute policy so improvements cannot be explained solely by extra inference/test budget.

## RQ4 — External validation
**Do benchmark-derived uncertainty categories explain human review friction in real agent-authored pull requests?**

**H4:** Specification, approach, implementation, testing, and operational uncertainty categories are associated with rejection, revision count, review duration, or human intervention in AIDev pull requests.

RQ4 is observational. Non-merge is not equivalent to incorrect code, and associations must not be described as causal effects.

## RQ5 — Model-family and access-regime portability
**How portable are stage-wise uncertainty estimates and selective-control gains across heterogeneous LLM families and access regimes?**

**H5:** A common black-box stage-wise representation exhibits smaller transfer degradation in discrimination, calibration, and control utility than endpoint-only confidence or model-specific uncertainty features under leave-one-model-family-out evaluation, with directionally consistent behavior on the frozen API robustness tier.

Primary analysis: leave-one-local-model-family-out across Qwen3-8B, Mistral-7B-Instruct-v0.3, and Gemma-3-12B-IT using only features available under black-box access.

Primary metrics: held-out-model AUROC retention, absolute ECE degradation, and change in success–cost area.

Secondary analysis: the frozen API subset is a portability stress test, not a provider leaderboard. Exact endpoint IDs, reasoning modes, access dates, and costs are frozen before sealed evaluation. Unexecuted API rows are reported as `N/A`, never estimated.
