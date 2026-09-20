## Cross-Model Interpretability Comparison

This section addresses Research Question 3 by quantifying and visualising the agreement and disagreement between the Logistic Regression and Random Forest global explanations. Two summary statistics anchor the comparison: the Spearman rank correlation between the two mean-|SHAP| vectors (Spearman, 1904), and the Jaccard index of the top-10 feature sets. Local-level agreement is then reported on the six illustrative cases from §4.7.

### Spearman Rank Correlation of the 44-Feature Importance Vectors

Across all 44 modelling features, the Spearman rank correlation between the two mean-|SHAP| vectors is 0.10 (p = 0.508, two-sided). The correlation is positive but small, and the p-value does not reject the null hypothesis of no rank correlation at conventional thresholds (α = 0.05). Read on its own, this single number would suggest that the two models pick out roughly the same features. The next two sub-sections show that the picture is more interesting once the magnitude asymmetry is corrected and the top-10 lists are inspected side by side.

### Side-by-Side Importance Bar Chart

Figure 13 plots the top-20 features by combined rank for both models. The two panels share the y-axis ordering but use different x-axis scales: the Logistic Regression panel is in log-odds units (range 0 to 3.0), the Random Forest panel is in probability units (range 0 to 0.15). The scales are not directly comparable in magnitude, but they are comparable in *rank*: the top rows are the most important features within each model, and the overlap of feature names reveals the cross-model agreement.

![Cross-model global importance bar chart, top 20 by combined rank](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/cross_model_importance.png){#fig:cross-model-importance}

**Figure 13**

*Cross-model global importance for the top 20 features by combined rank. Left: Logistic Regression, mean |SHAP| on log-odds scale. Right: Random Forest, mean |SHAP| on probability scale.*

*Note.* Spearman ρ = 0.10 (p = 0.508); top-10 Jaccard index = 0.25. The two panels share the y-axis ordering so the reader can compare ranks across models.

### Log-Log Scatter with Spearman Annotation

Figure 14 plots every one of the 44 features as a point with LR mean |SHAP| on the horizontal axis and RF mean |SHAP| on the vertical axis, both on a symlog scale. The top-10 features by LR mean |SHAP| are labelled. The scatter makes the same point as Figure 13 in a different visual idiom: features with high LR importance (right edge) cluster mostly in the upper half of the RF range, but the relationship is loose, with several features — `submission_rate` and `weighted_mean_score` in particular — that sit at the top of both models while the remainder are spread across the RF range.

![Cross-model feature importance scatter on log-log scale](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/cross_model_scatter.png){#fig:cross-model-scatter}

**Figure 14**

*Cross-model feature importance scatter on symlog axes. Each point is one feature; the top-10 by LR mean |SHAP| are labelled.*

*Note.* Both axes use symlog scaling to keep features with very small mean |SHAP| visible. Spearman ρ = 0.10 is the rank correlation of the 44 features.

### Top-10 Agreement and Divergence

Across the top-10 features in each model, four appear in both lists: `submission_rate`, `weighted_mean_score`, `edu_A Level or Equivalent`, and `gender_F`. The Jaccard index of the two sets is 0.25 (4 shared out of 16 unique). The six Logistic-Regression-only features are demographic and course-context: `edu_Lower Than A Level`, `module_GGG`, `gender_M`, `module_BBB`, `edu_HE Qualification`, and `region_East Anglian Region`. The six Random-Forest-only features are engagement and assessment: `assessments_submitted`, `mean_assessment_score`, `active_days`, `total_clicks`, `distinct_resources`, and `presentation_year`.

**Table 4**

*Top-10 feature agreement between Logistic Regression and Random Forest. A feature is listed under both models if it appears in that model's top-10 by mean |SHAP|.*

| Status | Features |
|--------|----------|
| In both top-10s | `submission_rate`, `weighted_mean_score`, `edu_A Level or Equivalent`, `gender_F` |
| LR-only in top-10 | `edu_Lower Than A Level`, `module_GGG`, `gender_M`, `module_BBB`, `edu_HE Qualification`, `region_East Anglian Region` |
| RF-only in top-10 | `assessments_submitted`, `mean_assessment_score`, `active_days`, `total_clicks`, `distinct_resources`, `presentation_year` |

*Note.* The 4 shared features are predominantly behavioural (engagement and assessment), while the 6 LR-only features are predominantly structural (demographic and course-context) and the 6 RF-only features are all behavioural.

### Local Direction Agreement Across the Six Cases

The cross-model agreement at the local level, computed on the six illustrative cases from §4.7, is reported in Table 5. The two models push the SHAP sum in the same direction for four of the six cases (TP, TN, FN, FP). They diverge in direction for the two borderline cases (Borderline-1 and Borderline-2), and they diverge in predicted label only for Borderline-1 (LR predicts Fail at 0.566; RF predicts Pass at 0.498).

**Table 5**

*Per-case local SHAP direction agreement between Logistic Regression and Random Forest on the six illustrative cases from §4.7.*

| Case | y_true | LR pred | RF pred | LR shift | RF shift | Same direction | Same label |
|------|--------|---------|---------|----------|----------|----------------|------------|
| TP | 1 | 1 | 1 | +8.24 | +0.500 | Yes | Yes |
| TN | 0 | 0 | 0 | −5.86 | −0.499 | Yes | Yes |
| FN | 1 | 0 | 0 | −3.41 | −0.465 | Yes | Yes |
| FP | 0 | 1 | 1 | +0.93 | +0.431 | Yes | Yes |
| Borderline-1 | 0 | 1 | 0 | +0.42 | −0.002 | No | No |
| Borderline-2 | 0 | 0 | 0 | +0.009 | −0.004 | No | Yes |

*Note.* LR shift is on the log-odds scale; RF shift is on the probability scale. The two scales differ, so the *direction* (sign) is what is comparable, not the magnitude.

### Synthesis Against Research Question 3

Logistic Regression and Random Forest identify substantially different factors as the drivers of student failure. The Spearman rank correlation is positive but not statistically distinguishable from zero, and the top-10 lists share only one feature in four. The Logistic Regression top-10 is dominated by demographic and course-context features; the Random Forest top-10 is dominated by engagement and assessment features. At the local level, the two models agree in direction for the four corners of the confusion matrix but disagree for the two borderline cases near the decision boundary. The two models do not identify the same factors, and what this implies is that the choice of model family changes both the global explanation and the local prediction. For institutional use, this matters: an early-warning system that runs Random Forest and one that runs Logistic Regression would flag somewhat different students and would offer somewhat different justifications. Whether the engagement-led or the demographic-led explanation is more useful depends on the institutional context, and that question is taken up in Chapter 5 §5.4.

A subtle point worth flagging at this stage, and one this study cannot resolve on its own: the cross-model divergence is partly a function of feature-engineering choices. Both models see the same 44 features, but the Logistic Regression sees them on a standardised scale, while the Random Forest sees them on their original scale. The TreeSHAP values, in particular, are not symmetric to the LinearSHAP values, and the disagreement in top-10 lists may partly reflect a scale-induced reordering rather than a fundamental epistemic disagreement between the two classifiers. A robustness check in which the Random Forest is also evaluated on the standardised features would clarify this, and that check is left for future work.
