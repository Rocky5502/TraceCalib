# Results Reporting Contract

TraceCalib-SE does not allow hand-edited numerical results. Every manuscript table cell and plotted point must originate from machine-readable outputs and carry provenance.

## RQ1
Generate failure-prediction and early-warning tables at 25%, 50%, 75%, and 100% trajectory progress. Compare TraceCalib-SE with verbal confidence, token likelihood/entropy, self-consistency, semantic/disagreement measures where available, simple trajectory statistics, and matched scalar temporal controls.

Required figures: AUROC/AUPRC over progress, reliability diagrams, and condition robustness.

## RQ2
Report stage-attribution Macro-F1, Top-1, Top-2, per-stage precision/recall, stage calibration, and transfer across held-out repositories. Include matched-capacity scalar and no-propagation controls.

Required figures: decomposition heatmap, stage confusion matrix, and repository/agent transfer view.

## RQ3
Compare stage-aware control against always-continue, static retry, test-failure-only repair, final-confidence abstention, stage-blind conformal control, random matched-budget intervention, and matched more-compute control.

Required figures: risk–coverage curve, success–cost frontier, and action-effectiveness plot.

A success-rate increase alone is not enough: the claim requires improvement on the matched-budget frontier.

## RQ4
Validate the uncertainty-category classifier on a manually labeled AIDev sample before using it for association analysis. Report classifier metrics, prevalence, and adjusted mixed-effects associations for merge/rejection, revisions, review duration, and human intervention.

Required figure: forest plot of adjusted associations with 95% intervals.

## RQ5
Run leave-one-model-family-out transfer across the three local model families using the frozen common black-box feature contract. Report in-family and held-out AUROC/AUPRC, Brier score, ECE, calibration slope/intercept, AUROC retention, ECE degradation, and success–cost-area delta.

The API tier is a secondary portability stress test. Report only endpoints actually executed under the frozen budget; unexecuted rows are `N/A`. Do not rank providers as a scientific objective.

Required outputs:
- `model_portability.long.csv`;
- `model_portability.json`;
- manuscript RQ5 model-portability table;
- vector model-family/API portability figure;
- cross-model-disagreement ablation when matched outputs exist.

## Provenance
Every generated table/figure must record Git commit, protocol freeze ID, dataset/model/agent revisions, run-manifest hash, timestamp, and script/config path.

## Negative results
Every RQ report must include the strongest counterexample, null/adverse result, and a bounded claim. Never delete a valid failed hypothesis merely because it weakens the preferred narrative.
