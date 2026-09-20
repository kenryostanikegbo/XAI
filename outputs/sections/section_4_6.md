## Global SHAP Interpretability

This section addresses Research Question 2 by ranking the features that drive the predictions of each model and by showing how each feature's value relates to its contribution to the prediction. The two visual encodings are: the beeswarm plot, which displays the per-instance SHAP distribution and a colour gradient for the feature value (Lundberg et al., 2020); and the mean-|SHAP| bar chart, which gives a compact ranking by overall contribution (Lundberg & Lee, 2017). The full per-feature values are reported in Appendix A.

### Logistic Regression — Global Importance

For Logistic Regression, the top three features by mean |SHAP| are `edu_A Level or Equivalent` (2.98), `edu_Lower Than A Level` (2.54), and `submission_rate` (2.40). Six of the ten most influential features are demographic or course-context variables — three education levels (`edu_*`), both gender indicators (`gender_F`, `gender_M`), and one module indicator (`module_GGG`). Only three engagement or assessment features reach the top ten: `submission_rate`, `weighted_mean_score`, and one module (`module_BBB`) that doubles as a course-context feature.

![Logistic Regression — SHAP beeswarm (scaled features)](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_summary_lr.png){#fig:shap-lr-summary}

**Figure 3**

*SHAP beeswarm for Logistic Regression over the held-out test set (n = 6,732). Each dot is one test instance; horizontal position is the SHAP contribution to the log-odds; colour encodes the scaled feature value (red = high, blue = low). The top 20 features are shown.*

*Note.* LinearSHAP returns values on the log-odds scale because the underlying model is a logistic regression; the magnitude of one log-odds shift is approximately equivalent to a probability shift of 0.21 at the mean prediction.

The beeswarm in Figure 3 reveals the direction of each feature's contribution as well as its magnitude. For the three education-level indicators, high values (red points) push the prediction toward Pass — that is, away from Fail — while low values (blue points) push it toward Fail. The same left-to-right reading applies to the engagement metrics: high `submission_rate`, `weighted_mean_score`, and the active-day indicators all push toward Pass. Reading across rows gives a clear pattern: the Logistic Regression leans on a small set of demographic and course-context features to make most of its decisions, and the contribution of each feature is roughly symmetric across instances.

![Logistic Regression — global feature importance (top 20 by mean |SHAP|)](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_importance_lr.png){#fig:shap-lr-importance}

**Figure 4**

*Mean |SHAP| (log-odds scale) for the top 20 features under Logistic Regression. Bars are sorted by descending importance.*

*Note.* The features above the line `region_South West Region` are all part of the Logistic Regression top-10; see Table 2 in §4.5 for the corresponding F1 and AUC values.

### Random Forest — Global Importance

The Random Forest reverses the priority. The top three features are `submission_rate` (mean |SHAP| = 0.148), `assessments_submitted` (0.076), and `mean_assessment_score` (0.070) — three engagement or assessment metrics in a row. Five of the top ten features are engagement or assessment metrics (`submission_rate`, `assessments_submitted`, `mean_assessment_score`, `weighted_mean_score`, `active_days`, `total_clicks`, `distinct_resources`, `mean_days_to_submit`). Only one demographic feature (`edu_A Level or Equivalent`) and one gender indicator (`gender_F`) break into the top ten.

![Random Forest — SHAP beeswarm (top 20 features)](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_summary_rf.png){#fig:shap-rf-summary}

**Figure 5**

*SHAP beeswarm for Random Forest over the stratified 300-row SHAP subsample. Each dot is one test instance; horizontal position is the SHAP contribution to the probability; colour encodes the original-scale feature value (red = high, blue = low).*

*Note.* TreeSHAP returns values on the probability scale because the underlying model is a probability classifier; the magnitude is approximately one probability unit per cent at the mean prediction. The subsample is stratified by class to preserve the 31.4 percent Fail prevalence of the full test set (Lundberg et al., 2020).

The beeswarm in Figure 5 shows much wider per-instance spreads than the Logistic Regression beeswarm. For `submission_rate`, the contribution extends from about −0.2 to about +0.2, depending on the instance, indicating that the Random Forest treats the same feature differently depending on its interaction with other features. The same is true for `assessments_submitted` and `mean_assessment_score`. The implication is that the Random Forest's predictions rely on interactions, which a linear model cannot capture.

![Random Forest — global feature importance (top 20 by mean |SHAP|)](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_importance_rf.png){#fig:shap-rf-importance}

**Figure 6**

*Mean |SHAP| (probability scale) for the top 20 features under Random Forest. Bars are sorted by descending importance.*

*Note.* The probability scale and log-odds scale are not directly comparable: a mean |SHAP| of 0.148 on the probability scale is roughly equivalent to a mean |SHAP| of 1.5 on the log-odds scale at the mean prediction.

### Methodological Note on the Two Explainers

The two explainers differ in three respects that matter for reading the figures. First, the LinearSHAP values are computed on the post-scaled features inside the Logistic Regression pipeline, while the TreeSHAP values are computed on the original-scale features (Lundberg & Lee, 2017). Second, the Logistic Regression beeswarm covers all 6,732 test instances, whereas the Random Forest beeswarm is restricted to a 300-row stratified subsample selected for tractability — the SHAP values for the same 300 rows are reused in §4.7. Third, the magnitude scales differ: the Logistic Regression values are in log-odds units, and the Random Forest values are in probability units. Direct cross-model ranking by raw mean |SHAP| is therefore not meaningful, and Chapter 4 §4.8 uses Spearman rank correlation on the per-feature ranks instead.

### Synthesis Against Research Question 2

Both models identify `submission_rate` and `weighted_mean_score` as the strongest drivers of student failure, which gives a degree of cross-model corroboration to the engagement-based hypothesis. Beyond that overlap, the two models diverge. The Logistic Regression top ten is dominated by demographic and course-context features, while the Random Forest top ten is dominated by engagement and assessment metrics. The two top-ten lists share only four features, and the rank-ordering of those four features also differs. The detailed quantification of this divergence, including the Spearman correlation of the full 44-feature importance vectors, is reported in Chapter 4 §4.8.

A subtle point worth flagging at this stage, and one this study cannot resolve on its own: the Random Forest's stronger reliance on engagement metrics may simply reflect the fact that tree ensembles can exploit non-linear interactions that a linear model misses, rather than a deeper truth about which features matter. The cross-model Spearman correlation reported in §4.8 provides the headline number; the local explanations in §4.7 reveal the per-instance pattern.
