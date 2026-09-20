## Methodology Recap

This section restates the methodological commitments that the analytical findings of §4.5–§4.9 depend on. The full methodology is documented in Chapter 3; the present section is a condensed reference for the reader who wants to interpret a figure or table without flipping back to Chapter 3 every few pages.

### Two Classifiers, One Shared Pipeline

Two classifiers are trained on the integrated matrix: a Logistic Regression with L2 regularisation and the l-bfgs solver, and a Random Forest with 500 trees and a maximum depth of 15 (Chapter 3 §3.7). Both classifiers are wrapped in an `imblearn.pipeline.Pipeline` that applies SMOTE inside each cross-validation fold before fitting, so that no test-fold information leaks into the training of any individual fold (Chapter 3 §3.6.4). Both classifiers are tuned by five-fold stratified grid search with `scoring='f1'`, and the best estimator is refit on the full training set before evaluation on the held-out test set.

### Logistic Regression Hyperparameters

The Logistic Regression grid covers the inverse regularisation strength `C ∈ {0.01, 0.1, 1, 10}`, with `penalty='l2'`, `solver='lbfgs'`, `class_weight=None`, and `max_iter=1000`. The `class_weight=None` choice is deliberate: SMOTE handles the class imbalance inside the pipeline, so the additional reweighting of `class_weight='balanced'` would double-count the imbalance handling (Chapter 3 §3.7.2). The best estimator after grid search uses `C=1.0`, the default value, which is consistent with the moderate size of the standardised feature space and the modest strength of the L2 penalty at that value.

### Random Forest Hyperparameters

The Random Forest grid covers `n_estimators ∈ {200, 500}`, `max_depth ∈ {None, 15, 25}`, and `min_samples_split ∈ {2, 5}`, with `class_weight=None`, `n_jobs=-1`, and `random_state=42`. The `n_estimators=500` setting was chosen as the upper end of the grid to minimise the variance of the predictions; `max_depth=15` was chosen to prevent overfitting on the training set while preserving the ability of the trees to capture non-linear interactions. The `min_samples_split=2` default is retained. The best estimator after grid search uses `n_estimators=500` and `max_depth=15`, which is the configuration used for all evaluations in §4.5.

### Class Imbalance Handling

SMOTE is applied inside the cross-validation loop with `k_neighbors=5` (the default) and `random_state=42` (Chapter 3 §3.6). The training set is balanced from 10,711 Pass / 4,906 Fail to 10,711 Pass / 10,711 Fail after SMOTE, and the validation fold in each cross-validation iteration is balanced in the same way before fitting. The test set is left at its original 31.4 per cent prevalence, and all reported metrics reflect the imbalanced deployment condition. This is a deliberate methodological choice: a model tuned and evaluated on a balanced test set would over-state its deployment performance on the imbalanced population.

### Evaluation Framework

Six metrics are reported in §4.5: accuracy, precision, recall, F1, ROC-AUC, and average precision (AP). Accuracy is the proportion of correct predictions and is reported for completeness but is not the primary metric because the 31.4 per cent class imbalance makes accuracy insensitive to the operationally important errors (failing students missed). Precision is the proportion of students flagged as failing who actually fail, and recall is the proportion of failing students who are flagged. F1 is the harmonic mean of precision and recall and is the metric on which both classifiers were tuned. ROC-AUC is the area under the receiver-operating-characteristic curve and is threshold-independent. AP is the area under the precision-recall curve and is more sensitive than ROC-AUC to performance on the minority class (Saito & Rehmsmeier, 2015).

### Cross-Validation and Final Evaluation

The cross-validation stage estimates the within-cohort performance of each classifier and selects the best hyperparameters. The final evaluation stage reports the held-out test performance of the refit estimator. The two stages are separated: the cross-validation metrics are not reported in §4.5 (they are available in notebook 04), and the held-out test metrics are reported exactly once. The test set is used exactly once, and the random seed is fixed at every stage of the pipeline so that a future reader can reproduce the cross-validation folds and the test-set predictions bit-for-bit.

### SHAP Computation

Two SHAP explainers are used: LinearSHAP for the Logistic Regression and TreeSHAP for the Random Forest (Chapter 3 §3.9). LinearSHAP returns values on the log-odds scale of the underlying linear model, and TreeSHAP returns values on the probability scale of the underlying tree ensemble. The two scales are not directly comparable in magnitude, but the sign of each SHAP value (push toward Pass or push toward Fail) is comparable across the two explainers, and the cross-model comparison in §4.8 is built on that comparability. The TreeSHAP computation is performed on a 300-row stratified subsample of the test set to keep the computation tractable; the LinearSHAP computation is performed on the full test set. The 300-row subsample is reused in §4.7 for the local explanations on the Random Forest side.

### Reproducibility

The methodology is reproducible from a clean clone of the repository in under 45 minutes on a standard laptop (Chapter 3 §3.10). The random seed is fixed at every stage of the pipeline, every notebook can be re-run from top to bottom without manual intervention, and every figure and table cited in this chapter is generated by the corresponding notebook and saved to `outputs/figures/` or `outputs/tables/`. The end-to-end reproducibility check is documented in Chapter 3 §3.10 and is the basis on which the present chapter's claims can be audited by a future reader.
