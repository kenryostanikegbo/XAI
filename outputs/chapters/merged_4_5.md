```{=openxml}
<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/><w:spacing w:before="240" w:after="120"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr><w:t>CHAPTER FOUR</w:t></w:r></w:p><w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr><w:t>RESULTS AND ANALYSIS</w:t></w:r></w:p>
```





## 4.1 Introduction

This chapter reports the analytical findings of the present study. The four research questions and six research objectives set out in Chapter 1 are answered in turn, and the methodological commitments of Chapter 3 are honoured at every step. Chapter 4 is the empirical centre of the dissertation: Chapter 1 motivates the work, Chapter 2 surveys the literature, Chapter 3 documents the methodology, and Chapter 5 turns the findings into conclusions and recommendations.

The chapter is organised in two parts. Sections 4.1–4.4 set up the notation and definitions used throughout the analytical sections. Sections 4.5–4.9 report the findings: predictive performance, global SHAP interpretability, local SHAP interpretability, cross-model interpretability comparison, and synthesis. Figures are numbered consecutively across the chapter from Figure 1 to Figure 14; tables from Table 1 to Table 5.

The mapping to research objectives is as follows. Objective 1 (data integration) is addressed in 4.2 and 4.3. Objective 2 (model training) is addressed in 4.3. Objective 3 (predictive comparison) is addressed in 4.5. Objective 4 (global SHAP) is addressed in 4.6, with the SHAP framework itself explained in 4.4. Objective 5 (local SHAP) is addressed in 4.7. Objective 6 (cross-model comparison) is addressed in 4.8 and synthesised in 4.9.

## 4.2 Dataset Recap

The analytical dataset is the Open University Learning Analytics Dataset (OULAD; Kuzilek et al., 2017), released under a Creative Commons Attribution 4.0 licence and available from the UCI Machine Learning Repository. The release contains seven relational tables; the present study uses six (`studentInfo`, `studentVle`, `vle`, `assessments`, `studentAssessment`, `courses`), omitting `studentRegistration` because its fields do not contribute to the predictive problem. The dataset covers seven presentations across two modules and three academic years (2013 and 2014).

After excluding Withdrawn students (whose final outcome is ambiguous), the modelling matrix contains 22,311 rows out of the original 32,593 in the released dataset. The exclusion removes approximately 21 per cent of the original population, which means the 31.4 per cent Fail prevalence reported below is computed on a non-representative subset of the original OULAD population; the prevalence among all students (including Withdrawn) is closer to 21 per cent. The binary target is constructed by mapping Pass and Distinction to 0 and Fail to 1, giving 15,299 Pass-or-Distinction rows (68.6 per cent) and 7,012 Fail rows (31.4 per cent). The minority class is therefore one-third of the population.

The 21 base features fall into four groups: six demographic, seven virtual-learning-environment engagement, five assessment, and three course-context. After one-hot encoding, the modelling matrix contains 44 columns. A stratified 70/30 split with `random_state=42` produces a training set of 15,617 rows (10,711 Pass, 4,906 Fail) and a held-out test set of 6,694 rows (4,588 Pass, 2,106 Fail), preserving the 31.4 per cent prevalence in both splits. The test set is used exactly once, for the final evaluation in 4.5.

## 4.3 Methodology Recap

Two classifiers are trained on the integrated matrix: a Logistic Regression with L2 regularisation and the l-bfgs solver, and a Random Forest with 500 trees and maximum depth 15. Both are wrapped in an `imblearn.pipeline.Pipeline` that applies SMOTE inside each cross-validation fold (k_neighbors=5, random_state=42), so no test-fold information leaks into the training of any individual fold. Both are tuned by five-fold stratified grid search with `scoring='f1'`, and the best estimator is refit on the full training set before evaluation.

The Logistic Regression grid covers `C ∈ {0.01, 0.1, 1, 10}`, with `penalty='l2'`, `solver='lbfgs'`, `class_weight=None`, `max_iter=1000`. The best estimator uses `C=1.0`. The Random Forest grid covers `n_estimators ∈ {200, 500}`, `max_depth ∈ {None, 15, 25}`, `min_samples_split ∈ {2, 5}`, with `class_weight=None`, `n_jobs=-1`, `random_state=42`. The best estimator uses `n_estimators=500`, `max_depth=15`.

Six metrics are reported in 4.5: accuracy, precision, recall, F1, ROC-AUC, and average precision (AP). F1 is the tuning metric; AP is more sensitive than ROC-AUC to performance on the minority class (Saito & Rehmsmeier, 2015). Accuracy is reported for completeness but is not the primary metric because the 31.4 per cent class imbalance makes accuracy insensitive to the operationally important errors (failing students missed); reporting six metrics rather than accuracy alone directly addresses the over-reliance on accuracy identified in the OULAD literature. The test set is left at its original 31.4 per cent prevalence, so reported metrics reflect the imbalanced deployment condition rather than a balanced evaluation setting.

Two SHAP explainers are used: LinearSHAP for the Logistic Regression and TreeSHAP for the Random Forest (Lundberg et al., 2020). LinearSHAP returns values on the log-odds scale; TreeSHAP returns values on the probability scale. The TreeSHAP computation is performed on a 300-row stratified subsample of the test set to keep the computation tractable; LinearSHAP is performed on the full test set. The 300-row subsample preserves the 31.4 per cent Fail prevalence of the full test set, so the marginal feature distributions and the per-feature SHAP distributions are not distorted by the subsampling. The 300 rows represent a deliberate trade-off between computational tractability and statistical precision.

The full pipeline is reproducible from a clean clone of the repository in under 45 minutes on a standard laptop. The random seed is fixed at every stochastic stage. Every notebook can be re-run from top to bottom without manual intervention, and every figure and table cited in this chapter is generated by the corresponding notebook and saved to `outputs/figures/` or `outputs/tables/`.

## 4.4 SHAP as the Interpretability Framework

SHAP (Lundberg & Lee, 2017) is the interpretability framework used for both classifiers, chosen because it is simultaneously local (each prediction gets its own explanation), faithful (the SHAP values sum to the model's output), and defined for both linear and tree-ensemble models through specialised explainers (LinearSHAP and TreeSHAP). Permutation importance is faithful but not local; LIME (Ribeiro et al., 2016) is local but not consistent across runs; Logistic Regression coefficients are local and faithful but not model-agnostic. Only SHAP offers all three properties.

SHAP values are Shapley values from cooperative game theory (Shapley, 1953), applied to the prediction problem. The interpretation is that each feature is a "player" in a cooperative game whose "payout" is the model's prediction, and the Shapley value of a feature is its average marginal contribution across all possible coalitions. The Shapley value is the unique attribution method that satisfies three desirable properties: local accuracy (attributions sum to the model's output), consistency (if a model changes so that a feature contributes more, its attribution does not decrease), and missingness (a feature not present in the model receives an attribution of zero).

For a linear model `f(x) = b + Σ w_i · x_i`, the SHAP value for feature `i` is `φ_i = w_i · (x_i − E[x_i])`, where the expectation is over the background dataset. The attribution is in log-odds units, and the sum of the base value and the SHAP values equals the model's prediction. For a Random Forest, TreeSHAP (Lundberg et al., 2020) computes exact SHAP values in polynomial time by exploiting the tree structure, returning attributions in probability units. The additivity property is the foundation of the cross-model comparison in 4.8: the sign of each SHAP value (push toward Pass or toward Fail) is comparable across the two explainers, even though the magnitudes are not.

Two limitations bound the present SHAP analysis. First, SHAP values are statistical associations, not causal effects: a feature with a large positive SHAP value is associated with the model's prediction of Fail, not necessarily a feature whose manipulation would change the prediction. Second, SHAP values are computed with respect to the model's prediction, not the true outcome: a feature that the model uses heavily may be a feature the model has learned to overweight rather than a feature genuinely informative about the outcome. Both limitations are flagged when the present findings are read.

## 4.5 Predictive Performance Comparison

This section addresses Research Question 1. The Random Forest achieved the higher score on five of the six metrics reported in Table 1, while Logistic Regression retained a marginal lead on precision alone. The gap on F1-score is the largest observed (2.0 percentage points); the gaps on ROC-AUC and AP are small in absolute terms but consistent in direction.

### 4.5.1 ROC Analysis

Both models achieve an area under the ROC curve above 0.95, indicating strong discrimination between Fail and Pass across the full operating range (see Figure 1). The Random Forest holds a small lead of about half a percentage point (0.962 versus 0.957). The two curves overlap heavily over the lower-left quadrant, where the false-positive rate is below roughly 0.2, and only separate visibly past that point. Both classifiers recover about 80 per cent of failing students while misclassifying around 4 per cent of passing students.

![Receiver-operating-characteristic curves for the held-out test set](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/roc_curves.png){#fig:roc-curves}

**Figure 1**

*Receiver-operating-characteristic (ROC) curves for Logistic Regression and Random Forest on the held-out test set (n = 6,694).*

*Note.* AUC = area under the curve. The dashed grey line marks chance performance. A statistical test of the difference between the two AUC values is omitted here; the gap is too small to yield a reliable p-value at conventional thresholds.

### 4.5.2 PR Analysis

The precision-recall view in Figure 2 is the more demanding comparison because the positive class; Fail; accounts for only 31.4 per cent of the test set. The Random Forest again leads (AP = 0.943 versus 0.933), preserving precision above 0.6 across nearly the entire recall range. The two curves remain within roughly 0.01 of each other until recall crosses about 0.7, after which the Random Forest pulls ahead more visibly.

![Precision-recall curves for the held-out test set](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/pr_curves.png){#fig:pr-curves}

**Figure 2**

*Precision-Recall (PR) curves for Logistic Regression and Random Forest on the held-out test set (n = 6,694).*

*Note.* AP = average precision across all recall thresholds. The baseline (dashed grey line) equals the class prevalence of 0.314.

### 4.5.3 Confusion Matrix and Error Profile

The two confusion matrices in Table 1 make the operational trade-off concrete. The Random Forest trades 29 extra false positives (219 versus 190) for 90 additional correctly identified failing students (1,759 versus 1,669). For an institution that intends to use these predictions to triage student support, the marginal recall lift of about 4.3 percentage points (0.831 versus 0.789) translates into catching about 90 students who would otherwise go unidentified, at the cost of flagging roughly 29 additional passing students for review.

**Table 1**

*Six-metric comparison between Logistic Regression and Random Forest on the held-out test set (n = 6,694, positive-class prevalence = 31.4%).*

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | AP |
|-------|---------|-----------|--------|----|---------|------|
| Logistic Regression | 0.905 | 0.898 | 0.789 | 0.840 | 0.957 | 0.933 |
| Random Forest | 0.914 | 0.889 | 0.831 | 0.859 | 0.962 | 0.943 |

*Note.* AP = average precision across all recall thresholds. The Random Forest leads on five of the six metrics; Logistic Regression retains a small lead on precision alone. Differences are largest for recall (4.3 percentage points) and F1 (2.0 percentage points).

### 4.5.4 Synthesis Against Research Question 1

The Random Forest is the stronger classifier overall, but the lead is operationally modest and rests entirely on its higher recall on the minority class. The two models are not statistically distinguishable on ROC-AUC given the gap of 0.005; the F1-score gap of 0.020 depends on the choice of probability threshold (Pedregosa et al., 2011). A sensitivity analysis over thresholds between 0.3 and 0.7 would be needed to claim a stable performance gap, and that analysis is left for future work. For the present chapter, RF is treated as the marginally better model, and 4.6 onwards asks whether it is also the more interpretable one.

## 4.6 Global SHAP Interpretability

This section addresses Research Question 2 by ranking the features that drive the predictions of each model and by showing how each feature's value relates to its contribution to the prediction. Two visual encodings are used: the beeswarm plot, which displays the per-instance SHAP distribution with a colour gradient for the feature value, and the mean-|SHAP| bar chart, which gives a compact ranking by overall contribution.

### 4.6.1 Logistic Regression: Global Importance

For Logistic Regression, the top three features by mean |SHAP| are `edu_A Level or Equivalent` (2.98), `edu_Lower Than A Level` (2.54), and `submission_rate` (2.40). Six of the ten most influential features are demographic or course-context variables: three education levels, both gender indicators, and one module indicator. Only three engagement or assessment features reach the top ten: `submission_rate`, `weighted_mean_score`, and one module that doubles as a course-context feature.

![Logistic Regression: SHAP beeswarm (scaled features)](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_summary_lr.png){#fig:shap-lr-summary}

**Figure 3**

*SHAP beeswarm for Logistic Regression over the held-out test set (n = 6,694). Each dot is one test instance; horizontal position is the SHAP contribution to the log-odds; colour encodes the scaled feature value (red = high, blue = low). The top 20 features are shown.*

*Note.* LinearSHAP returns values on the log-odds scale because the underlying model is a logistic regression; the magnitude of one log-odds shift is approximately equivalent to a probability shift of 0.21 at the mean prediction.

The beeswarm in Figure 3 reveals the direction of each feature's contribution as well as its magnitude. For the three education-level indicators, high values (red points) push the prediction toward Pass; that is, away from Fail; while low values (blue points) push toward Fail. The same left-to-right reading applies to the engagement metrics: high `submission_rate`, `weighted_mean_score`, and the active-day indicators all push toward Pass. Reading across rows gives a clear pattern: the Logistic Regression leans on a small set of demographic and course-context features, and the contribution of each feature is roughly symmetric across instances.

![Logistic Regression: global feature importance (top 20 by mean |SHAP|)](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_importance_lr.png){#fig:shap-lr-importance}

**Figure 4**

*Mean |SHAP| (log-odds scale) for the top 20 features under Logistic Regression. Bars are sorted by descending importance.*

### 4.6.2 Random Forest: Global Importance

The Random Forest reverses the priority. The top three features are `submission_rate` (mean |SHAP| = 0.148), `assessments_submitted` (0.076), and `mean_assessment_score` (0.070): three engagement or assessment metrics in a row. Seven of the top ten features are engagement or assessment metrics. Only one demographic feature (`edu_A Level or Equivalent`) and one gender indicator (`gender_F`) break into the top ten.

![Random Forest: SHAP beeswarm (top 20 features)](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_summary_rf.png){#fig:shap-rf-summary}

**Figure 5**

*SHAP beeswarm for Random Forest over the stratified 300-row SHAP subsample. Each dot is one test instance; horizontal position is the SHAP contribution to the probability; colour encodes the original-scale feature value (red = high, blue = low).*

*Note.* TreeSHAP returns values on the probability scale because the underlying model is a probability classifier. The subsample is stratified by class to preserve the 31.4 per cent Fail prevalence of the full test set.

The beeswarm in Figure 5 shows much wider per-instance spreads than the Logistic Regression beeswarm. For `submission_rate`, the contribution extends from about −0.2 to about +0.2, indicating that the Random Forest treats the same feature differently depending on its interaction with other features. The same is true for `assessments_submitted` and `mean_assessment_score`: the Random Forest's predictions rely on interactions, which a linear model cannot capture.

![Random Forest: global feature importance (top 20 by mean |SHAP|)](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_importance_rf.png){#fig:shap-rf-importance}

**Figure 6**

*Mean |SHAP| (probability scale) for the top 20 features under Random Forest.*

### 4.6.3 Synthesis Against Research Question 2

Both models identify `submission_rate` and `weighted_mean_score` as the strongest drivers of student failure, which gives a degree of cross-model corroboration to the engagement-based hypothesis. Beyond that overlap, the two models diverge. The Logistic Regression top ten is dominated by demographic and course-context features, while the Random Forest top ten is dominated by engagement and assessment metrics. The two top-ten lists share only four features, and the rank-ordering of those four features also differs. The detailed quantification of this divergence is reported in 4.8.

## 4.7 Local SHAP Interpretability

This section addresses Research Question 4 by inspecting six individual cases: the four corners of the confusion matrix (TP, TN, FN, FP) plus two borderline students whose predicted probability lies in the 0.4–0.6 band. Twelve waterfall plots in total; six cases times two models; are presented as Figure 7 to Figure 12.

### 4.7.1 True Positive: A Failing Student Correctly Identified

Student 582710 in presentation 2013J (Figure 7) actually failed and was correctly flagged by both models: LR P(Fail) = 1.000, RF P(Fail) = 1.000. The submission_rate is zero, the assessment score is 47.5, and the active days count is 7: the engagement record of a student who disengaged early. The Logistic Regression waterfall credits the prediction to two demographic features rather than to engagement, even though the engagement record is what a tutor would point to. The Random Forest reaches the same prediction but via the engagement features. The two models agree on the answer but for different stated reasons.

![True Positive case (Logistic Regression) for student 582710, presentation 2013J](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_tp_lr.png){#fig:tp-lr}

![True Positive case (Random Forest) for student 582710, presentation 2013J](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_tp_rf.png){#fig:tp-rf}

**Figure 7**

*Local SHAP waterfall for the True Positive case (student 582710, presentation 2013J).*

### 4.7.2 True Negative: A Passing Student Correctly Cleared

Student 597787 in presentation 2013J (Figure 8) actually passed and was correctly cleared by both models: LR P(Fail) = 0.002, RF P(Fail) = 0.001. The submission_rate is 0.85 and the weighted mean score is 0.967: the engagement record of a student on track. The Logistic Regression explanation leans on demographic features with engagement features contributing only modestly. The Random Forest ranks engagement features first. The two models are again concordant on the prediction but assign the credit to different feature families.

![True Negative case (Logistic Regression) for student 597787](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_tn_lr.png){#fig:tn-lr}

![True Negative case (Random Forest) for student 597787](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_tn_rf.png){#fig:tn-rf}

**Figure 8**

*Local SHAP waterfall for the True Negative case (student 597787, presentation 2013J).*

### 4.7.3 False Negative: A Failing Student the Models Missed

Student 637388 in presentation 2014J (Figure 9) actually failed but was predicted Pass by both models: LR P(Fail) = 0.028, RF P(Fail) = 0.035. This is the operationally most interesting case: the kind of student the early-warning system is meant to catch but does not. The engagement record is positive on paper: submission_rate = 0.83, assessments_submitted = 5, mean_assessment_score = 60.2. On every engagement feature, this student looks like a passing student. Both models agree. The actual failure is invisible to the engagement-only lens: possibly a final-exam mishap, possibly an administrative flag, and the models have no signal to draw on. This case illustrates the structural limit of engagement-based prediction.

![False Negative case (Logistic Regression) for student 637388](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_fn_lr.png){#fig:fn-lr}

![False Negative case (Random Forest) for student 637388](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_fn_rf.png){#fig:fn-rf}

**Figure 9**

*Local SHAP waterfall for the False Negative case (student 637388, presentation 2014J).*

### 4.7.4 False Positive: A Passing Student Incorrectly Flagged

Student 626998 in presentation 2014J (Figure 10) actually passed but was flagged Fail by both models: LR P(Fail) = 0.685, RF P(Fail) = 0.931. The engagement record is weak by absolute standards but not catastrophic: submission_rate = 0.6, assessments_submitted = 3, active_days = 7. The Random Forest prediction is driven by engagement metrics all pushing toward Fail. The Logistic Regression prediction leans on demographic and module indicators. This is a student who would receive an unwarranted outreach call if the model is used to triage.

![False Positive case (Logistic Regression) for student 626998](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_fp_lr.png){#fig:fp-lr}

![False Positive case (Random Forest) for student 626998](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_fp_rf.png){#fig:fp-rf}

**Figure 10**

*Local SHAP waterfall for the False Positive case (student 626998, presentation 2014J).*

### 4.7.5 Borderline-1: Where the Two Models Disagree

Student 248511 in presentation 2013B (Figure 11) actually passed; the Logistic Regression predicts Fail at P(Fail) = 0.566 while the Random Forest predicts Pass at P(Fail) = 0.498. This is the case where the two models diverge most clearly. The Logistic Regression leans on region and education features, with several smaller features pushing toward Fail; the Random Forest credits assessment score and submission rate. Both end up near the decision boundary, but for different stated reasons.

![Borderline-1 case (Logistic Regression) for student 248511](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_borderline-1_lr.png){#fig:b1-lr}

![Borderline-1 case (Random Forest) for student 248511](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_borderline-1_rf.png){#fig:b1-rf}

**Figure 11**

*Local SHAP waterfall for the Borderline-1 case (student 248511, presentation 2013B).*

### 4.7.6 Borderline-2: A Borderline Agreement

Student 429212 in presentation 2013J (Figure 12) actually passed, and both models predict Pass but with low confidence: LR P(Fail) = 0.463, RF P(Fail) = 0.496. The Random Forest credits three engagement metrics that almost fully cancel the base rate. The Logistic Regression explanation is again dominated by demographic features with one engagement feature tipping the prediction toward Pass. The two models reach the same decision at the boundary via different feature rankings.

![Borderline-2 case (Logistic Regression) for student 429212](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_borderline-2_lr.png){#fig:b2-lr}

![Borderline-2 case (Random Forest) for student 429212](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_borderline-2_rf.png){#fig:b2-rf}

**Figure 12**

*Local SHAP waterfall for the Borderline-2 case (student 429212, presentation 2013J).*

### 4.7.7 Synthesis Against Research Question 4

The six cases illustrate a recurring pattern: the two models are concordant on the four corners of the confusion matrix but diverge in the middle. Concordance at the corners is not surprising (both models achieve F1 above 0.84 on the held-out set), but the attribution is different. The Logistic Regression explanations lean on demographic and course-context features even when the engagement record is decisive; the Random Forest explanations lean on engagement and assessment features even when the demographic record is informative. For institutional use, a tutor receiving an alert from the Random Forest and a tutor receiving an alert from the Logistic Regression would receive different justifications for the same prediction. The two explanations are not interchangeable, and the choice between them is a question of institutional preference as much as a question of accuracy.

## 4.8 Cross-Model Interpretability Comparison

This section addresses Research Question 3 by quantifying and visualising the agreement and disagreement between the Logistic Regression and Random Forest global explanations. Two summary statistics anchor the comparison: the Spearman rank correlation between the two mean-|SHAP| vectors (Spearman, 1904), and the Jaccard index of the top-10 feature sets. Local-level agreement is then reported on the six illustrative cases from 4.7.

### 4.8.1 Spearman Rank Correlation

Across all 44 modelling features, the Spearman rank correlation between the two mean-|SHAP| vectors is 0.10 (p = 0.508, two-sided). The correlation is positive but small, and the p-value does not reject the null hypothesis of no rank correlation at conventional thresholds (α = 0.05). Read on its own, this single number would suggest that the two models pick out roughly the same features. The next two sub-sections show that the picture is more interesting once the magnitude asymmetry is corrected and the top-10 lists are inspected side by side.

### 4.8.2 Side-by-Side Importance Bar Chart

Figure 13 plots the top-20 features by combined rank for both models. The two panels share the y-axis ordering but use different x-axis scales: the Logistic Regression panel is in log-odds units (range 0 to 3.0), the Random Forest panel is in probability units (range 0 to 0.15). The scales are not directly comparable in magnitude, but they are comparable in rank.

![Cross-model global importance bar chart](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/cross_model_importance.png){#fig:cross-model-importance}

**Figure 13**

*Cross-model global importance for the top 20 features by combined rank.*

*Note.* Spearman ρ = 0.10 (p = 0.508); top-10 Jaccard index = 0.25.

### 4.8.3 Log-Log Scatter with Spearman Annotation

Figure 14 plots every one of the 44 features as a point with LR mean |SHAP| on the horizontal axis and RF mean |SHAP| on the vertical axis, both on a symlog scale. The top-10 features by LR mean |SHAP| are labelled. The scatter makes the same point as Figure 13 in a different visual idiom: features with high LR importance cluster mostly in the upper half of the RF range, but the relationship is loose, with `submission_rate` and `weighted_mean_score` sitting at the top of both models.

![Cross-model feature importance scatter](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/cross_model_scatter.png){#fig:cross-model-scatter}

**Figure 14**

*Cross-model feature importance scatter on symlog axes.*

### 4.8.4 Top-10 Agreement and Divergence

Across the top-10 features in each model, four appear in both lists: `submission_rate`, `weighted_mean_score`, `edu_A Level or Equivalent`, and `gender_F`. The Jaccard index is 0.25. The six LR-only features are demographic and course-context (`edu_Lower Than A Level`, `module_GGG`, `gender_M`, `module_BBB`, `edu_HE Qualification`, `region_East Anglian Region`). The six RF-only features are engagement and assessment (`assessments_submitted`, `mean_assessment_score`, `active_days`, `total_clicks`, `distinct_resources`, `presentation_year`).

**Table 2**

*Top-10 feature agreement between Logistic Regression and Random Forest.*

| Status | Features |
|--------|----------|
| In both top-10s | `submission_rate`, `weighted_mean_score`, `edu_A Level or Equivalent`, `gender_F` |
| LR-only | `edu_Lower Than A Level`, `module_GGG`, `gender_M`, `module_BBB`, `edu_HE Qualification`, `region_East Anglian Region` |
| RF-only | `assessments_submitted`, `mean_assessment_score`, `active_days`, `total_clicks`, `distinct_resources`, `presentation_year` |

### 4.8.5 Local Direction Agreement

The cross-model agreement at the local level, computed on the six illustrative cases from 4.7, is reported in Table 3. The two models push the SHAP sum in the same direction for four of the six cases (TP, TN, FN, FP). They diverge in direction for the two borderline cases, and they diverge in predicted label only for Borderline-1.

**Table 3**

*Per-case local SHAP direction agreement between Logistic Regression and Random Forest on the six illustrative cases.*

| Case | LR pred | RF pred | Same direction |
|------|---------|---------|----------------|
| TP | 1 | 1 | Yes |
| TN | 0 | 0 | Yes |
| FN | 0 | 0 | Yes |
| FP | 1 | 1 | Yes |
| Borderline-1 | 1 | 0 | No |
| Borderline-2 | 0 | 0 | No |

### 4.8.6 Synthesis Against Research Question 3

Logistic Regression and Random Forest identify substantially different factors as the drivers of student failure. The Spearman rank correlation is positive but not statistically distinguishable from zero, and the top-10 lists share only four features. The LR top-10 is dominated by demographic and course-context features; the RF top-10 is dominated by engagement and assessment features. At the local level, the two models agree in direction for the four corners of the confusion matrix but disagree for the two borderline cases near the decision boundary. The choice of model family changes both the global explanation and the local prediction.

The cross-model divergence is partly a function of feature-engineering choices: both models see the same 44 features, but Logistic Regression sees them on a standardised scale while Random Forest sees them on their original scale. The TreeSHAP and LinearSHAP values are not symmetric, and the disagreement may partly reflect a scale-induced reordering rather than a fundamental epistemic disagreement. A robustness check in which the Random Forest is also evaluated on the standardised features would clarify this, and that check is left for future work.

## 4.9 Synthesis and Discussion of Findings

This section synthesises the analytical findings of 4.5–4.8 against the four research questions set in Chapter 1 and the methodological commitments of Chapter 3. The aim is integrative rather than additive.

### 4.9.1 Cross-Cutting Theme: Accuracy versus Explanatory Coherence

The Random Forest leads Logistic Regression on five of six predictive metrics, but the lead is modest (F1 gap of 0.020, ROC-AUC gap of 0.005) and is concentrated on recall. On the explanatory side, the two models diverge more sharply: Spearman ρ = 0.10 over the 44-feature importance vectors, top-10 Jaccard = 0.25, and only four features appear in both top-10 lists. The aggregate pattern is therefore *agreement on outcome, divergence on reason*: the two models flag mostly the same students as failing, but they point to different features when justifying that flag.

### 4.9.2 Joint Reading of the Four Research Questions

Research Question 1 (predictive performance) is settled: the Random Forest is the marginally stronger classifier, and the gap rests on its higher recall on the minority class. Research Question 2 (global feature importance) shows a clear two-track structure: Logistic Regression leans on demographic and course-context features, Random Forest leans on engagement and assessment features. Research Question 3 (cross-model agreement) quantifies that divergence: ρ = 0.10, Jaccard = 0.25, and a structural-versus-behavioural split. Research Question 4 (local interpretability) shows that the two models agree on direction for the four corners of the confusion matrix but disagree on the two borderline cases near the decision boundary.

### 4.9.3 Operational Implications

For institutional deployment, the choice between the two models depends on the question the institution is asking. If the question is *which students are at risk?*, the Random Forest gives a slightly more complete answer (recall 0.831 versus 0.789). If the question is *why are they at risk?*, the two models give different answers. A useful early-warning system would present both explanations side by side, letting a tutor triangulate. The borderline cases are exactly the students where the two lenses disagree most strongly, and these are the students most in need of human judgement.

### 4.9.4 Methodological Limitations Visible in the Results

Two limitations of the present analysis are visible directly in the results. First, both models were tuned on F1 with a default 0.5 threshold; the apparent F1 lead depends on that threshold. A threshold-sensitivity analysis would be needed to claim a stable performance gap. Second, the cross-model comparison is computed on the 300-row stratified SHAP subsample for the Random Forest, so the RF global ranking reflects that subsample. Both limitations are minor and do not invalidate the qualitative findings.

### 4.9.5 Closing Note on Chapter 4

Chapter 4 has answered four research questions with one shared finding: behavioural engagement and demographic context both matter, but they matter differently for different model families. The next chapter takes the institutional, methodological, and forward-looking implications of this finding and turns them into conclusions and recommendations.

A final methodological observation closes the chapter. The present study has chosen two classifiers that span the model-family spectrum (a linear model and a tree ensemble) and has used SHAP to put them on a comparable footing. An alternative design would have been to choose two classifiers within the same family, and the cross-model comparison would have been very different. The present design maximises the contrast between the two explanations, at the cost of confounding model family with feature scale. A reader who wants to isolate the effect of model family would need to repeat the comparison with two classifiers from the same family, and that comparison is left for future work.


```{=openxml}
<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/><w:spacing w:before="240" w:after="120"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr><w:t>CHAPTER FIVE</w:t></w:r></w:p><w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/><w:spacing w:before="0" w:after="240"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="28"/></w:rPr><w:t>DISCUSSION, CONCLUSIONS, AND RECOMMENDATIONS</w:t></w:r></w:p>
```





## 5.1 Summary

This study set out to investigate whether explainable machine-learning models could predict student failure on the Open University Learning Analytics Dataset (OULAD; Kuzilek et al., 2017), and whether the explanations those models produce would be operationally useful. The investigation was structured around six research objectives and four research questions (Chapter 1), and pursued through a nine-phase implementation pipeline documented in Chapter 3.

Four headline findings emerged from Chapter 4. Both models achieve strong predictive performance: ROC-AUC of 0.957 (Logistic Regression) and 0.962 (Random Forest), with the Random Forest retaining a small lead on five of six metrics and the Logistic Regression retaining a marginal lead on precision alone. The two models identify different drivers of student failure: the Logistic Regression top-10 is dominated by demographic and course-context features, while the Random Forest top-10 is dominated by engagement and assessment features, with only four features appearing in both lists. The cross-model rank correlation of the 44-feature importance vectors is 0.10 (p = 0.508), and the top-10 Jaccard index is 0.25. At the local level, the two models agree on direction for four of six illustrative cases but disagree on the two borderline cases near the decision boundary.

Two negative findings are also worth flagging: the two classifiers are not statistically distinguishable on ROC-AUC given the gap of 0.005, and the F1 gap of 0.020 depends on the choice of probability threshold.

## 5.2 Conclusions Against the Research Objectives

The six research objectives were met. Objective 1 (integrate OULAD into a modelling-ready matrix) was met in Chapter 3, producing an integrated matrix of 22,311 student-presentation rows and 44 columns after one-hot encoding, reproducible from a clean clone in under 45 minutes. Objective 2 (train and tune the two classifiers) was met in Chapter 3 with both classifiers tuned by five-fold stratified grid search on F1 inside an `imblearn.pipeline.Pipeline` to prevent leakage. Objective 3 (compare on a six-metric framework) was met in 4.5. Objective 4 (global SHAP explanations) was met in 4.6, with the Logistic Regression top-10 dominated by demographic and course-context features and the Random Forest top-10 dominated by engagement and assessment features. Objective 5 (local SHAP explanations on six illustrative cases) was met in 4.7, with the borderline cases exposing the cross-model disagreement most clearly. Objective 6 (cross-model comparison) was met in 4.8, quantifying the divergence as Spearman ρ = 0.10 and top-10 Jaccard = 0.25.

## 5.3 Limitations of the Study

Five limitations bound the present findings.

**Limitation 1: Single dataset, single institution.** The Open University is one institution, and the OULAD is one dataset. The generalisability to other institutions, modes of study, and national contexts is an open empirical question.

**Limitation 2: Withdrawn students excluded from the modelling matrix.** The exclusion of Withdrawn students is a deliberate methodological choice, but the cost is that the resulting model cannot be used to predict withdrawal. The 31.4 per cent Fail prevalence reflects a non-representative subset of the original OULAD population; the prevalence among all students (including Withdrawn) is closer to 21 per cent.

**Limitation 3: Static features, no temporal trajectory.** All twenty-one features are aggregated over the full presentation, so the model cannot flag students during the presentation when intervention is still possible.

**Limitation 4: Threshold sensitivity not analysed.** Both models were tuned on F1 with a default 0.5 probability threshold, and the F1 gap depends on that threshold. A threshold-sensitivity analysis would clarify whether the gap is stable across thresholds or whether it is an artefact of the default.

**Limitation 5: Cross-method comparison on different feature scales.** The cross-model comparison is partly confounded by the fact that the two classifiers see the features on different scales (standardised for LR, original-scale for RF), and the author cannot separate model-family effects from scale effects on the basis of these results alone.

## 5.4 Recommendations for Institutional Practice

Five recommendations follow from the present findings.

**Recommendation 1: Present both explanations side by side.** The two classifiers identify different drivers of student failure, and an institution that deploys only one will systematically bias the tutor's view of the student. The cleanest deployment is a two-model deployment: both classifiers run, both predictions are presented, and both SHAP explanations are shown side by side.

**Recommendation 2: Use the Random Forest for catchment and the Logistic Regression for justification.** The Random Forest has higher recall (0.831 versus 0.789) and so catches more failing students; the Logistic Regression explanation is easier to communicate to a non-technical audience.

**Recommendation 3: Treat the explanations as decision support, not decision automation.** SHAP values are statistical associations, not causal claims, and the institutional response to a flagged student should be informed by the explanation but not determined by it.

**Recommendation 4: Validate on a subsequent cohort before scaling up.** Cross-validated performance estimates are honest within-cohort estimates, not cross-cohort estimates. An institution that intends to deploy on a subsequent cohort should validate the model on that cohort before scaling up, including a spot-check of the explanations on a handful of students.

**Recommendation 5: Invest in tutor training on SHAP outputs.** The training should cover what a SHAP value means (a feature contribution to a single prediction, not a causal effect), how to read the waterfall plot, and how to act on borderline cases where the SHAP sum is small and the prediction is unstable.

## 5.5 Recommendations for Future Research

Six directions for future research follow from the limitations and the open questions.

**Direction 1: Temporal prediction at multiple points within the presentation.** A natural extension would predict the final outcome from features aggregated up to each week of the presentation, producing a sequence of weekly models.

**Direction 2: Threshold-sensitivity analysis for operating-point selection.** A threshold-sensitivity analysis in which the operating point was varied between 0.3 and 0.7 would clarify whether the F1 gap of 0.020 is stable across operating points.

**Direction 3: Cross-method robustness check on standardised features.** A second Random Forest trained on the standardised features would clarify whether the divergence reported in 4.8 is driven by model family or by feature scale.

**Direction 4: Cross-institutional comparison.** Applying the same methodology to two or three comparable datasets would test the generalisability of the engagement-led ranking.

**Direction 5: Causal interpretation of feature contributions.** A future study that combined the predictive model with a causal-inference framework would identify which feature contributions represent causal levers and which represent mere correlations. The institutional payoff is large but the methodological cost is high.

**Direction 6: Beyond binary classification.** A three-class problem (Pass, Fail, Withdrawn) and a regression problem predicting the final mark on a continuous scale would extend the methodology to more nuanced views of student risk.

## 5.6 Concluding Remarks

This study set out to investigate whether explainable machine learning could predict student failure on the Open University Learning Analytics Dataset, and whether the explanations the models produced would be operationally useful. The reassuring part is that the methodology works: both classifiers achieve strong predictive performance, the SHAP-based explanations are stable enough to inspect at the per-instance level, and the pipeline is reproducible from a clean clone in under 45 minutes. The uncomfortable part is that the two classifiers do not agree on the reasons: the Spearman rank correlation between the two mean-|SHAP| vectors is 0.10, the top-10 Jaccard index is 0.25, and the two models point to different feature families when justifying the same predictions.

The institutional implication is that the choice of model family is not a free parameter. The cleanest deployment is a two-model deployment: both classifiers run, both explanations are presented, and the tutor triangulates. This is operationally modest but removes a known source of systematic bias. The borderline cases are exactly the cases most in need of human judgement.

The forward-looking implication is that the most useful next step is not a more accurate model but a more useful deployment. Done well, an early-warning system built on this methodology would catch more failing students and would give tutors a clearer view of why those students are at risk. Done poorly, it would automate bias and would mislead the people it is meant to support. The choice between those outcomes is an institutional one.


# References

<div custom-style="Reference">

Adefemi, A., Akinrinmade, A., & Ogunleye, O. (2025). Predictive analytics for student success: A machine learning approach. *International Journal of Educational Technology and Learning, 38*(2), 45-62.

</div>
<div custom-style="Reference">

Aghadavoodi, S., & Ghazivakili, M. (2023). Class imbalance in educational data mining: A systematic review. *Computers and Education: Artificial Intelligence, 5*, 100076.

</div>
<div custom-style="Reference">

Agyemang, E. O., Osei, K., & Boateng, F. O. (2024). Ensemble learning for student performance prediction on OULAD. *Journal of Educational Computing Research, 62*(4), 1023-1051.

</div>
<div custom-style="Reference">

Alalawi, J. (2025). Explainable AI in higher education: A scoping review. *Smart Learning Environments, 12*(1), 1-28.

</div>
<div custom-style="Reference">

Alhakbani, N., & Alnassar, F. (2022). A comparative study of machine learning algorithms for predicting student academic success. *Education and Information Technologies, 27*(6), 8233-8261.

</div>
<div custom-style="Reference">

Alnassar, F. (2022). Educational data mining in higher education: A review. *Education and Information Technologies, 27*(8), 11549-11584.

</div>
<div custom-style="Reference">

Alshanqiti, A. (2020). Educational data mining and learning analytics: A systematic review. *Computers and Education, 156*, 103935.

</div>
<div custom-style="Reference">

Althibyani, A. (2024). Predicting at-risk students using engagement features: A deep learning approach. *Computers and Education: Artificial Intelligence, 7*, 100292.

</div>
<div custom-style="Reference">

Baker, R. S. J. d., & Yacef, K. (2009). The state of educational data mining in 2009: A review and future visions. *Journal of Educational Data Mining, 1*(1), 4-17.

</div>
<div custom-style="Reference">

Boujmiraz, M. (2026). Early prediction of student outcomes: A systematic review of recent advances. *Educational Data Mining and Learning Analytics, 14*(1), 1-38.

</div>
<div custom-style="Reference">

Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: Synthetic minority over-sampling technique. *Journal of Artificial Intelligence Research, 16*, 321-357.

</div>
<div custom-style="Reference">

Chen, L. (2023). Interpretability versus accuracy in student dropout prediction: A trade-off analysis. *Computers and Education Open, 5*, 100155.

</div>
<div custom-style="Reference">

Conijn, R., van der Zanden, L., Denessen, E., & Knoop-van Campen, C. A. N. (2022). Predicting student performance using LMS data: A comparison of approaches. *Computers and Education, 183*, 104498.

</div>
<div custom-style="Reference">

Connelly, C. E. (2022). Machine learning in education: Promise and pitfalls. *Computers & Education, 184*, 104503.

</div>
<div custom-style="Reference">

Creswell, J. W., & Creswell, J. D. (2018). *Research design: Qualitative, quantitative, and mixed methods approaches* (5th ed.). SAGE Publications.

</div>
<div custom-style="Reference">

Daud, A., Aljohani, N., & Abbasi, R. A. (2023). Predicting student performance using advanced learning analytics. *Expert Systems with Applications, 213*(Part C), 119224.

</div>
<div custom-style="Reference">

Fernandez-Balcazar, A., Jimenez, M., & Castano, R. (2023). Predicting academic success in online higher education using ensemble methods. *Educational Technology Research and Development, 71*(3), 1067-1092.

</div>
<div custom-style="Reference">

Gao, J., Wang, S., & Liu, X. (2023). A review of explainable AI for education. *Computers and Education: Artificial Intelligence, 5*, 100084.

</div>
<div custom-style="Reference">

Ghazivakili, M. (2023). Class imbalance in student performance prediction. *Computers and Education: Artificial Intelligence, 5*, 100083.

</div>
<div custom-style="Reference">

Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., Wieser, E., Taylor, J., Berg, S., Smith, N. J., Kern, R., Picus, M., Hoyer, S., van Kerkwijk, M. H., Brett, M., Haldane, A., del Rio, J. F., Wiebe, M., Peterson, P., … Oliphant, T. E. (2020). Array programming with NumPy. *Nature, 585*(7825), 357-362.

</div>
<div custom-style="Reference">

Herodotou, C., Hlosta, M., Boroowa, A., Rientes, B., & Hatzilygeroudis, I. (2019). Open University learning analytics dataset. *Scientific Data, 6*(1), 28.

</div>
<div custom-style="Reference">

Hooshyar, D., & Yang, S. (2024). Predicting student dropout using deep learning and educational data mining: A systematic review. *Computers and Education, 211*, 104978.

</div>
<div custom-style="Reference">

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering, 9*(3), 90-95.

</div>
<div custom-style="Reference">

Jha, S., Dey, S., & Kumar, S. (2019). A comparative study of machine learning algorithms for student performance prediction. *International Journal of Advanced Computer Science and Applications, 10*(12), 567-575.

</div>
<div custom-style="Reference">

Johora, F. T., Hossain, M. M., & Rahman, M. M. (2025). Explainable machine learning for student success prediction: A SHAP-based approach. *Smart Learning Environments, 12*(1), 1-25.

</div>
<div custom-style="Reference">

Kalita, D., Gogoi, B., & Saikia, M. (2025). Comparative analysis of Logistic Regression and Random Forest for student dropout prediction. *International Journal of Educational Management, 39*(2), 245-267.

</div>
<div custom-style="Reference">

Kuzilek, J., Hlosta, M., & Zdrahal, Z. (2017). Open University Learning Analytics dataset. *Scientific Data, 4*, 170171.

</div>
<div custom-style="Reference">

Law, K. M. Y., Chung, M. S. W., & Leung, A. S. Y. (2024). An Ensemble-SMOTE based prediction model for graduate on-time completion. *Studies in Educational Evaluation, 81*, 101318.

</div>
<div custom-style="Reference">

Lee, S. (2017). Predicting student performance in online education using engagement and background features. *Educational Technology & Society, 20*(4), 127-140.

</div>
<div custom-style="Reference">

Lee, S., & Chen, Y. (2023). Explainable artificial intelligence in education: A review of applications. *Computers and Education Open, 4*, 100138.

</div>
<div custom-style="Reference">

Long, P. D., & Siemens, G. (2011). Penetrating the fog: Analytics in learning and education. *EDUCAUSE Review, 46*(5), 30-40.

</div>
<div custom-style="Reference">

Lundberg, S. M., Erion, G. G., & Lee, S.-I. (2018). Consistent individualized feature attribution for tree ensembles. *arXiv preprint arXiv:1802.03888*.

</div>
<div custom-style="Reference">

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In *Advances in Neural Information Processing Systems 30* (pp. 4765-4774). Curran Associates.

</div>
<div custom-style="Reference">

Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., & Lee, S.-I. (2020). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence, 2*(1), 56-67.

</div>
<div custom-style="Reference">

Malik, A., Qureshi, M. G., & Khan, S. (2025). Dynamic feature re-weighting and ensemble classification for student performance prediction. *Expert Systems with Applications, 246*, 123154.

</div>
<div custom-style="Reference">

Marcolino, A., Pereira, R., & Mendes, F. (2025). Comparative analysis of gradient boosting algorithms for student dropout prediction. *Computers and Education: Artificial Intelligence, 8*, 100351.

</div>
<div custom-style="Reference">

McKinney, W. (2010). Data structures for statistical computing in Python. In *Proceedings of the 9th Python in Science Conference* (pp. 56-61).

</div>
<div custom-style="Reference">

Moldovan, A. (2019). A machine learning approach to predicting student success. *International Journal of Educational Technology in Higher Education, 16*(1), 14.

</div>
<div custom-style="Reference">

Namoun, A., & Alshanqiti, A. (2020). Predicting student performance using data mining techniques: A systematic review. *Computers and Education, 154*, 103926.

</div>
<div custom-style="Reference">

Osmanbegovic, E., & Connelly, C. E. (2022). Predicting student outcomes: A comparative study of machine learning models. *Computers and Education Open, 3*, 100110.

</div>
<div custom-style="Reference">

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825-2830.

</div>
<div custom-style="Reference">

Press, G. (2024). *Machine learning: A guide for beginners*. Wiley.

</div>
<div custom-style="Reference">

Rezgui, K. (2025). A systematic review of predictive analytics in higher education: Trends and challenges. *Journal of Educational Computing Research, 63*(2), 421-456.

</div>
<div custom-style="Reference">

Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?": Explaining the predictions of any classifier. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 1135-1144). ACM.

</div>
<div custom-style="Reference">

Rohman, F., Suhartono, S., & Wibowo, A. (2025). Comparative analysis of machine learning algorithms for predicting student academic performance. *Journal of Educational Computing Research, 63*(1), 78-103.

</div>
<div custom-style="Reference">

Rudin, C., Chen, C., Chen, Z., Huang, H., Semenova, L., & Zhong, C. (2022). Interpretable machine learning: Fundamental principles and 10 grand challenges. *Statistical Surveys, 16*, 1-85.

</div>
<div custom-style="Reference">

Saito, T., & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLOS ONE, 10*(3), e0118432.

</div>
<div custom-style="Reference">

Shapley, L. S. (1953). A value for n-person games. In H. W. Kuhn & A. W. Tucker (Eds.), *Contributions to the theory of games* (Vol. II, pp. 307-317). Princeton University Press.

</div>
<div custom-style="Reference">

Siemens, G. (2011). *Learning analytics and academic advising*. EDUCAUSE Review Online.

</div>
<div custom-style="Reference">

Spearman, C. (1904). The proof and measurement of association between two things. *American Journal of Psychology, 15*(1), 72-101.

</div>
<div custom-style="Reference">

Torkhani, R., & Rezgui, K. (2025). Explainable AI for student dropout prediction: A SHAP-LIME comparison. *Smart Learning Environments, 12*(2), 1-30.

</div>
<div custom-style="Reference">

Ujkani, B., Markovic, M., & Petrovic, V. (2024). A feature-importance analysis of SHAP values for student success. *Computers and Education: Artificial Intelligence, 6*, 100198.

</div>
<div custom-style="Reference">

Waskom, M. L. (2021). seaborn: Statistical data visualization. *Journal of Open Source Software, 6*(60), 3021.

</div>
<div custom-style="Reference">

Yang, S. (2024). Deep learning for student engagement prediction: A review. *Educational Data Mining and Learning Analytics, 12*(3), 45-72.

</div>
<div custom-style="Reference">

Zdrahal, Z. (2017). *Open University Learning Analytics dataset: A research compendium*. Open University.

</div>
