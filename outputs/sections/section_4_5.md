## Predictive Performance Comparison

This section addresses Research Question 1 by reporting Precision, Recall, F1-score, ROC-AUC, and Average Precision (AP) for both models on the held-out test set, and by comparing the two classifiers using the receiver-operating-characteristic (ROC) and precision-recall (PR) curves shown in Figure 1 and Figure 2.

The Random Forest achieved the higher score on five of the six metrics reported in Table 2, while Logistic Regression retained a marginal lead on precision alone. The gap on F1-score is the largest one observed; the gaps on ROC-AUC and AP are small in absolute terms but consistent in direction.

### ROC Analysis

Both models achieve an area under the ROC curve above 0.95, indicating strong discrimination between Fail and Pass across the full operating range (see Figure 1). The Random Forest holds a small lead of about half a percentage point (0.962 versus 0.957). The two curves overlap heavily over the lower-left quadrant of the plot, where the false-positive rate is below roughly 0.2, and only separate visibly past that point. In practical terms, both classifiers recover about 80 percent of the failing students while only misclassifying around 4 percent of passing students as failures.

![Receiver-operating-characteristic curves for the held-out test set](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/roc_curves.png){#fig:roc-curves}

**Figure 1**

*Receiver-operating-characteristic (ROC) curves for Logistic Regression and Random Forest on the held-out test set (n = 6,732).*

*Note.* AUC = area under the curve. The dashed grey line marks chance performance. A statistical test of the difference between the two AUC values is omitted here; the gap is too small to yield a reliable p-value at conventional thresholds.

### PR Analysis

The precision-recall view in Figure 2 is the more demanding comparison because the positive class — Fail — accounts for only 31.4 percent of the test set. Under that framing, the Random Forest again leads (AP = 0.943 versus 0.933), preserving precision above 0.6 across nearly the entire recall range. The two curves remain within roughly 0.01 of each other until recall crosses about 0.7, after which the Random Forest pulls ahead more visibly.

![Precision-recall curves for the held-out test set](C:/Users/HomePC/Documents/reportwritingprojects/studnetxai/outputs/figures/pr_curves.png){#fig:pr-curves}

**Figure 2**

*Precision-Recall (PR) curves for Logistic Regression and Random Forest on the held-out test set (n = 6,732).*

*Note.* AP = average precision across all recall thresholds. The baseline (dashed grey line) equals the class prevalence of 0.314.

### Confusion Matrix and Error Profile

The two confusion matrices in Table 2 make the operational trade-off concrete. The Random Forest trades 29 extra false positives (219 versus 190) for 90 additional correctly identified failing students (1,759 versus 1,669). For an institution that intends to use these predictions to triage student support, the marginal recall lift of about 4.3 percentage points (0.831 versus 0.789) translates into catching about 90 students who would otherwise go unidentified, at the cost of flagging roughly 29 additional passing students for review.

**Table 2**

*Six-metric comparison between Logistic Regression and Random Forest on the held-out test set (n = 6,732, positive-class prevalence = 31.4%).*

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | AP |
|-------|---------|-----------|--------|----|---------|------|
| Logistic Regression | 0.905 | 0.898 | 0.789 | 0.840 | 0.957 | 0.933 |
| Random Forest | 0.914 | 0.889 | 0.831 | 0.859 | 0.962 | 0.943 |

*Note.* AP = average precision across all recall thresholds. The Random Forest leads on five of the six metrics; Logistic Regression retains a small lead on precision alone. Differences are largest for recall (4.3 percentage points) and F1 (2.0 percentage points).

### Synthesis Against Research Question 1

The Random Forest is the stronger classifier overall, but the lead is operationally modest and rests entirely on its higher recall on the minority class. The two models are not statistically distinguishable on ROC-AUC at conventional thresholds given the gap of 0.005; the F1-score gap of 0.020, while larger, depends on the choice of probability threshold (default 0.5) used by `predict()` (Pedregosa et al., 2011). A sensitivity analysis over thresholds between 0.3 and 0.7 would be needed to claim a stable performance gap, and that analysis is left for future work (see Chapter 5 §5.5). For the present chapter, RF is treated as the marginally better model, and Chapter 4 §4.6 onwards asks whether it is also the more interpretable one.

A subtle point worth flagging here, and one this study cannot resolve on its own: both models were tuned for F1, so the apparent F1 lead of the Random Forest may partly reflect favourable noise in the train/test split despite the use of stratified cross-validation. Operating both models against an external validation cohort, drawn from a subsequent presentation year, would be the cleanest next step.
