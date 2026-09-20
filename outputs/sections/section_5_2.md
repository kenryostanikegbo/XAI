## Conclusions Against the Research Objectives

Chapter 1 §1.5 set six research objectives. Each is restated below and answered against the findings of Chapter 4.

### Objective 1 — Integrate the OULAD Tables into a Modelling-Ready Matrix

The first objective was to integrate the seven OULAD tables into a single modelling-ready matrix (Chapter 1 §1.5.1). This objective was met in Chapter 3 §3.4–§3.5 and in notebooks 01 and 02. The integrated matrix contained 22,311 student-presentation rows (after excluding Withdrawn), 21 base features, and 44 columns after one-hot encoding. The full pipeline is reproducible from a clean clone in under 45 minutes on a standard laptop, satisfying the reproducibility commitment of Chapter 1 §1.6. The data integration is not a contribution of this study in itself — others have integrated OULAD before (Kuzilek et al., 2017) — but it is the foundation on which the predictive and explanatory contributions rest, and it is documented at a level of detail that should allow a third party to reproduce every column of the modelling matrix from the raw CSVs alone.

### Objective 2 — Train and Tune Two Classifiers on a Held-Out Test Set

The second objective was to train and tune Logistic Regression and Random Forest classifiers on the integrated matrix using a rigorous pipeline that avoided data leakage (Chapter 1 §1.5.2). This objective was met in Chapter 3 §3.7 and in notebook 04. Both classifiers were tuned by five-fold stratified grid search on F1, with SMOTE applied within each fold to avoid leakage, and both were refit on the full training set before evaluation. The held-out test set was used exactly once, for the final evaluation in §4.5. The pipeline is reproducible and the random seed is documented at every stage, satisfying the methodological commitments of Chapter 3 §3.10.

### Objective 3 — Compare the Two Classifiers on a Six-Metric Framework

The third objective was to compare the two classifiers on a six-metric framework that includes both threshold-dependent metrics (precision, recall, F1) and threshold-independent metrics (ROC-AUC, average precision) plus accuracy (Chapter 1 §1.5.3). This objective was met in Chapter 4 §4.5. The Random Forest achieved the higher score on five of the six metrics and the Logistic Regression retained a marginal lead on precision alone. The gap was operationally modest and concentrated on recall; the two classifiers were not statistically distinguishable on ROC-AUC. The comparison was reported in the form of receiver-operating-characteristic curves and precision-recall curves, allowing a future reader to inspect the trade-off at any operating point they care about.

### Objective 4 — Explain Both Classifiers at the Global Level Using SHAP

The fourth objective was to apply SHAP to both classifiers at the global level and to rank the features that drive the predictions (Chapter 1 §1.5.4). This objective was met in Chapter 4 §4.6. The beeswarm plot and the mean-|SHAP| bar chart were produced for both classifiers, and the rankings were saved as CSV files for downstream reuse. The Logistic Regression top-10 was found to be dominated by demographic and course-context features; the Random Forest top-10 was found to be dominated by engagement and assessment features. The detailed rankings are reported in Appendix A and in the supplementary materials.

### Objective 5 — Explain Both Classifiers at the Local Level Using SHAP

The fifth objective was to apply SHAP to both classifiers at the local level on six illustrative cases (Chapter 1 §1.5.5). This objective was met in Chapter 4 §4.7. The six cases were the four corners of the confusion matrix (true positive, true negative, false negative, false positive) plus two borderline students whose predicted probability lay in the 0.4–0.6 band. The local SHAP waterfall plots were produced for all twelve case-model combinations, and the narratives describing each case were written directly into the prose. The borderline cases were particularly informative: they exposed the cross-model disagreement most clearly, and they showed that the choice of model family can change the predicted label for a student whose feature values lie near the decision boundary.

### Objective 6 — Compare the Global and Local Explanations Across the Two Classifiers

The sixth objective was to compare the global and local explanations across the two classifiers, and to quantify the agreement and disagreement (Chapter 1 §1.5.6). This objective was met in Chapter 4 §4.8. The Spearman rank correlation between the two mean-|SHAP| vectors was 0.10 (p = 0.508, not statistically significant), and the top-10 Jaccard index was 0.25. The four shared features were `submission_rate`, `weighted_mean_score`, `edu_A Level or Equivalent`, and `gender_F`. The local-direction agreement was 4 of 6 cases, with disagreement concentrated on the borderline students. The cross-model comparison is the distinctive contribution of this study: it answers the question of whether the two classifiers identify the same factors, and the answer is no — they identify different factors, and the difference is concentrated on the structural-versus-behavioural axis.
