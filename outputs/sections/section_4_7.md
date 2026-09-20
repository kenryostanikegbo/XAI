## Local SHAP Interpretability

This section addresses Research Question 4 by inspecting six individual cases — the four corners of the confusion matrix (TP, TN, FN, FP) plus two borderline students whose predicted probability lies in the 0.4–0.6 band. For each case, both models are shown side by side: the Logistic Regression waterfall operates on the log-odds scale, the Random Forest waterfall on the probability scale. Twelve waterfall plots in total — six cases times two models — are presented as Figure 7 to Figure 12 below. The six cases are drawn from the 300-row stratified SHAP subsample so that every per-instance SHAP value is already computed; the subsample preserves the 31.4 percent Fail prevalence of the full test set.

### True Positive — A Failing Student Correctly Identified

Student 582710 in presentation 2013J (Figure 7) actually failed and was correctly flagged by both models: Logistic Regression returned P(Fail) = 1.000, Random Forest returned P(Fail) = 1.000. The submission_rate is zero, the assessment score is 47.5, and the active days count is 7 — the engagement record of a student who disengaged early. The Logistic Regression waterfall credits the prediction to two demographic features (`region_Yorkshire Region` at −7.19, pushing toward Pass, then cancelled by `edu_A Level or Equivalent` at +2.98 pushing toward Fail) rather than to engagement, even though the engagement record is what a tutor would point to. The Random Forest reaches the same prediction but via the engagement features: `submission_rate` (+0.14), `assessments_submitted` (+0.09), and `active_days` (+0.06) push toward Fail; `module_GGG` and `gender_F` push weakly the other way. The two models agree on the answer but for different stated reasons — the Logistic Regression credits demographics, the Random Forest credits engagement.

![True Positive case (Logistic Regression and Random Forest) for student 582710, presentation 2013J](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_tp_lr.png){#fig:tp-lr}

![True Positive case (Random Forest) for student 582710, presentation 2013J](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_tp_rf.png){#fig:tp-rf}

**Figure 7**

*Local SHAP waterfall for the True Positive case (student 582710, presentation 2013J; y = Fail, both models predicted Fail).*

*Note.* Both panels share the y-axis categories, but only the top contributors are shown; the bottom row aggregates the remaining 30 features. LR values are on the log-odds scale; RF values are on the probability scale.

### True Negative — A Passing Student Correctly Cleared

Student 597787 in presentation 2013J (Figure 8) actually passed and was correctly cleared by both models: Logistic Regression P(Fail) = 0.002, Random Forest P(Fail) = 0.001. The submission_rate is 0.85 and the weighted mean score is 0.967 — the engagement record of a student on track. The Logistic Regression explanation leans heavily on demographic features again (`region_London Region` at −7.37, `module_FFF` at −3.13, `edu_A Level or Equivalent` at −2.98, all pushing toward Pass), with engagement features contributing only modestly (`submission_rate` at −2.10). The Random Forest ranks engagement features first (`mean_assessment_score` at +0.16, `weighted_mean_score` at +0.13) but, in this case, those are pushing the prediction toward Fail, not toward Pass; it is `submission_rate` (−0.11) and `assessments_submitted` (−0.08) that ultimately swing the prediction to Pass. The two models are again concordant on the prediction but assign the credit to different feature families.

![True Negative case (Logistic Regression) for student 597787, presentation 2013J](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_tn_lr.png){#fig:tn-lr}

![True Negative case (Random Forest) for student 597787, presentation 2013J](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_tn_rf.png){#fig:tn-rf}

**Figure 8**

*Local SHAP waterfall for the True Negative case (student 597787, presentation 2013J; y = Pass, both models predicted Pass).*

*Note.* Logistic Regression pushes toward Fail via education and module indicators; Random Forest pushes toward Pass via engagement metrics. The two models reach the same prediction through different feature sets.

### False Negative — A Failing Student the Models Missed

Student 637388 in presentation 2014J (Figure 9) actually failed but was predicted Pass by both models: Logistic Regression P(Fail) = 0.028, Random Forest P(Fail) = 0.035. This is the operationally most interesting case — the kind of student the early-warning system is meant to catch but does not. The engagement record is positive on paper: submission_rate = 0.83, assessments_submitted = 5, mean_assessment_score = 60.2, weighted_mean_score = 73.75, active_days = 111, total_clicks = 2,300. On every engagement feature, this student looks like a passing student. Both models agree. The actual failure is invisible to the engagement-only lens — possibly a final-exam mishap, possibly an administrative flag — and the models have no signal to draw on. The single feature that points toward Fail in the Random Forest is `module_BBB` (+0.07 in the LR waterfall, +0.04 in the RF waterfall): a course-context indicator that lifts the failure probability by a few percentage points but not enough to flip the prediction. This case illustrates the structural limit of engagement-based prediction.

![False Negative case (Logistic Regression) for student 637388, presentation 2014J](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_fn_lr.png){#fig:fn-lr}

![False Negative case (Random Forest) for student 637388, presentation 2014J](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_fn_rf.png){#fig:fn-rf}

**Figure 9**

*Local SHAP waterfall for the False Negative case (student 637388, presentation 2014J; y = Fail, both models predicted Pass).*

*Note.* Every engagement feature pushes toward Pass; both models are systematically blind to the actual cause of failure.

### False Positive — A Passing Student Incorrectly Flagged

Student 626998 in presentation 2014J (Figure 10) actually passed but was flagged Fail by both models: Logistic Regression P(Fail) = 0.685, Random Forest P(Fail) = 0.931. The engagement record is weak by absolute standards but not catastrophic: submission_rate = 0.6, assessments_submitted = 3, active_days = 7, total_clicks = 58, distinct_resources = 11. The Random Forest prediction is driven by `submission_rate` (+0.12), `assessments_submitted` (+0.12), `active_days` (+0.09), and `total_clicks` (+0.07), all pushing toward Fail. The Logistic Regression prediction leans on demographic and module indicators: `region_Yorkshire Region` (−7.19 toward Pass, but cancelled by other features), `module_EEE` (−4.16 toward Pass), and `edu_A Level or Equivalent` (+2.98 toward Fail). This is a student who would receive an unwarranted outreach call if the model is used to triage.

![False Positive case (Logistic Regression) for student 626998, presentation 2014J](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_fp_lr.png){#fig:fp-lr}

![False Positive case (Random Forest) for student 626998, presentation 2014J](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_fp_rf.png){#fig:fp-rf}

**Figure 10**

*Local SHAP waterfall for the False Positive case (student 626998, presentation 2014J; y = Pass, both models predicted Fail).*

*Note.* Random Forest confidence is much higher (0.93) than Logistic Regression (0.69); the underlying feature attributions are also more concentrated on engagement metrics.

### Borderline-1 — Where the Two Models Disagree

Student 248511 in presentation 2013B (Figure 11) actually passed; the Logistic Regression predicts Fail at P(Fail) = 0.566 while the Random Forest predicts Pass at P(Fail) = 0.498. This is the case where the two models diverge most clearly, and the local explanation illustrates the difference in reasoning: the Logistic Regression leans on `region_South West Region` (−7.76 toward Pass) and `edu_A Level or Equivalent` (−2.98 toward Pass), with several smaller features pushing toward Fail (`gender_M` +2.28, `module_GGG` +1.50). The Random Forest credits `mean_assessment_score` (+0.13 toward Fail), then pulls back with `submission_rate` (−0.11 toward Pass) and `weighted_mean_score` (+0.10 toward Fail, then offset). The two explanations are roughly mirror images: the Logistic Regression explanation is dominated by demographic features whose contributions almost cancel, while the Random Forest explanation is dominated by engagement features that also almost cancel. Both end up near the decision boundary, but for different stated reasons.

![Borderline-1 case (Logistic Regression) for student 248511, presentation 2013B](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_borderline-1_lr.png){#fig:b1-lr}

![Borderline-1 case (Random Forest) for student 248511, presentation 2013B](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_borderline-1_rf.png){#fig:b1-rf}

**Figure 11**

*Local SHAP waterfall for the Borderline-1 case (student 248511, presentation 2013B; y = Pass; LR predicts Fail at 0.566, RF predicts Pass at 0.498).*

*Note.* Both models are near the decision boundary, but the SHAP decomposition shows they get there from different feature families.

### Borderline-2 — A Borderline Agreement

Student 429212 in presentation 2013J (Figure 12) actually passed, and both models predict Pass but with low confidence: Logistic Regression P(Fail) = 0.463, Random Forest P(Fail) = 0.496. The two models agree on the label but for different feature-based reasons. The Random Forest credits `submission_rate` (−0.13 toward Pass), `mean_assessment_score` (−0.08 toward Pass), and `assessments_submitted` (−0.08 toward Pass) — three engagement metrics that almost fully cancel the base rate. The Logistic Regression explanation is again dominated by demographic features (`region_South West Region` −7.76, `edu_HE Qualification` −4.85, `module_DDD` −2.92) with one engagement feature (`submission_rate` −1.51) tipping the prediction toward Pass. The two models reach the same decision at the boundary via different feature rankings.

![Borderline-2 case (Logistic Regression) for student 429212, presentation 2013J](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_borderline-2_lr.png){#fig:b2-lr}

![Borderline-2 case (Random Forest) for student 429212, presentation 2013J](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/shap_local_borderline-2_rf.png){#fig:b2-rf}

**Figure 12**

*Local SHAP waterfall for the Borderline-2 case (student 429212, presentation 2013J; y = Pass; LR predicts Pass at 0.463, RF predicts Pass at 0.496).*

*Note.* Low confidence on both sides, but the feature attributions remain different in style.

### Cross-Model Local Agreement

Across the six cases, the two models push the SHAP sum in the same direction for four of the six (TP, TN, FN, FP). They diverge in direction for the two borderline cases (Borderline-1 and Borderline-2), and they diverge in predicted label only for Borderline-1 (LR predicts Fail, RF predicts Pass). The FN case — the operationally most important — is the cleanest local agreement: both models systematically underestimate the failure risk because the engagement record is misleadingly positive. The Borderline-1 disagreement suggests that, for students near the decision boundary, the choice of model family can change the predicted label, with Logistic Regression leaning more on demographic features and Random Forest more on engagement features.

### Synthesis Against Research Question 4

The six cases illustrate a recurring pattern: the two models are concordant on the four corners of the confusion matrix but diverge in the middle. Concordance at the corners is not surprising — both models achieve F1 above 0.84 on the held-out set — but the attribution is different. The Logistic Regression explanations lean on demographic and course-context features even when the engagement record is decisive; the Random Forest explanations lean on engagement and assessment features even when the demographic record is informative. For institutional use, the implication is that a tutor receiving an alert from the Random Forest and a tutor receiving an alert from the Logistic Regression would receive different justifications for the same prediction. The two explanations are not interchangeable, and the choice between them is a question of institutional preference as much as a question of accuracy.
