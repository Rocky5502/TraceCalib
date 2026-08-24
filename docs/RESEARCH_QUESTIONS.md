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
