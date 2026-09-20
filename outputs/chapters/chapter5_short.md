# Chapter 5: Discussion, Conclusions, and Recommendations

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
