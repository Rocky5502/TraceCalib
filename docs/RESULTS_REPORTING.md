# Results Reporting Contract

TraceCalib-SE does not allow hand-edited numerical results. Every manuscript table cell and plotted point must originate from machine-readable outputs and carry provenance.

## RQ1
Generate failure-prediction and early-warning tables at 25%, 50%, 75%, and 100% trajectory progress. Compare TraceCalib-SE with verbal confidence, token likelihood/entropy, self-consistency, semantic/disagreement measures where available, simple trajectory statistics, and matched scalar temporal controls.

Required figures:
- AUROC/AUPRC versus trajectory progress;
- reliability diagrams with bin counts and confidence bands;
- condition robustness plot.

## RQ2
Report stage-attribution Macro-F1, Top-1, Top-2, per-stage precision/recall, stage calibration, and transfer across held-out repositories. Include matched-capacity scalar and no-propagation controls.

Required figures:
- stage-by-failure decomposition heatmap;
- stage confusion matrix;
- cross-repository/model/agent transfer heatmap.

## RQ3
Compare stage-aware control against always-continue, static retry, test-failure-only repair, final-confidence abstention, stage-blind conformal control, random matched-budget intervention, and matched more-compute control.

Required figures:
- risk–coverage curve;
- success–cost frontier;
- action-effectiveness plot.

A success-rate increase alone is not enough: the claim requires improvement on the matched-budget frontier.

## RQ4
Validate the uncertainty-category classifier on a manually labeled AIDev sample before using it for association analysis. Report classifier metrics, prevalence, and adjusted mixed-effects associations for merge/rejection, revisions, review duration, and human intervention.

Required figure:
- forest plot of adjusted associations with 95% intervals.

## Provenance
Every generated table/figure must record:
- Git commit;
- protocol freeze ID;
- dataset/model/agent revisions;
- run-manifest hash;
- timestamp;
- script path and config path.

## Negative results
Every RQ report must include the strongest counterexample, null/adverse result, and a bounded claim. Never delete a valid failed hypothesis merely because it weakens the preferred narrative.
