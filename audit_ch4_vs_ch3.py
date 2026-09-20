"""Audit: does Chapter 4 capture every method Chapter 3 says will be implemented?"""
import re

with open('chapter3_text.txt', encoding='utf-8') as f:
    ch3 = f.read()
with open('outputs/chapters/chapter4.md', encoding='utf-8') as f:
    ch4 = f.read()

checks = [
    # (label, chapter3 phrase/claim, search-term-in-ch4, is_present_expected)
    ("OULAD source: UCI repo",          "UCI Machine Learning Repository",        "UCI",                              "mention"),
    ("Six OULAD tables used",            "six linked tables",                       "studentInfo",                       "mention"),
    ("Target: binary Pass/Fail",        "binary target",                           "binary target",                     "mention"),
    ("Fail as positive class",          "positive class",                          "Fail",                              "mention"),
    ("Distinction merged into Pass",   "Distinction into Pass",                   "Distinction",                       "mention"),
    ("Withdrawn excluded",              "Withdrawn",                               "Withdrawn",                         "mention"),
    ("k_neighbors=5 in SMOTE",          "k = 5",                                   "k_neighbors",                       "explicit"),
    ("SMOTE only on training",          "exclusively to the training partition",   "inside each cross-validation fold","explicit"),
    ("70/30 stratified split",          "70%",                                    "70",                                "explicit"),
    ("random_state=42",                 "fixed random seed (42)",                  "random_state=42",                   "explicit"),
    ("5-fold stratified CV",            "five-fold stratified cross-validation",   "five-fold",                          "explicit"),
    ("GridSearchCV",                    "GridSearchCV",                            "grid search",                       "explicit"),
    ("F1 as tuning metric",             "F1-score",                                "F1",                                "explicit"),
    ("LR grid: C",                      "Logistic Regression",                     "C",                                 "explicit"),
    ("RF grid: n_estimators",           "n_estimators",                            "n_estimators",                      "explicit"),
    ("RF grid: max_depth",              "max_depth",                               "max_depth",                         "explicit"),
    ("Six metrics reported",            "four-metric",                             "Precision, Recall, F1",             "explicit"),
    ("Accuracy NOT sole criterion",     "explicitly rejects accuracy",             "accuracy is reported",              "mention"),
    ("Confusion matrix reported",       "confusion matrix",                        "Confusion Matrix",                  "explicit"),
    ("ROC-AUC",                         "ROC-AUC",                                 "ROC-AUC",                           "explicit"),
    ("PR curve reported",               "(implied via ROC-AUC + AP)",              "Precision-Recall",                  "explicit"),
    ("SHAP / LinearSHAP",               "linear implementation",                   "LinearSHAP",                        "explicit"),
    ("SHAP / TreeSHAP",                 "TreeSHAP",                                "TreeSHAP",                          "explicit"),
    ("Beeswarm plot",                   "summary (beeswarm)",                      "beeswarm",                          "explicit"),
    ("Mean |SHAP| bar chart",           "mean absolute SHAP value bar",            "mean |SHAP|",                       "explicit"),
    ("Local waterfall plots",           "SHAP waterfall and force",                "waterfall",                         "explicit"),
    ("Local cases: at least 1 FN",      "at least one false negative",             "False Negative",                    "explicit"),
    ("Spearman correlation",            "Spearman rank correlation",               "Spearman",                          "explicit"),
    ("Cross-model comparison",          "comparative analysis",                    "cross-model",                       "explicit"),
    ("Top features comparison",         "agreement in their top-ranked",           "top-10",                            "explicit"),
    ("Reproducibility",                 "exactly reproducible",                    "reproducib",                        "explicit"),
    ("Single fixed seed",               "single fixed random seed",                "random_state=42",                   "explicit"),
    ("Implementation: Python+Jupyter",  "Jupyter notebooks",                       "(not expected in Ch4 prose)",       "absent"),
    ("pandas/NumPy used",               "pandas",                                  "(not expected in Ch4 prose)",       "absent"),
    ("scikit-learn used",               "scikit-learn",                            "(not expected in Ch4 prose)",       "absent"),
    ("imbalanced-learn used",           "imbalanced-learn",                        "imblearn",                          "mention"),
    ("matplotlib/seaborn used",         "matplotlib",                              "(not expected in Ch4 prose)",       "absent"),
    ("shap library used",               "shap library",                            "shap",                              "mention"),
    ("Ethics: anonymised, no contact",  "fully anonymised",                        "(not expected in Ch4 prose)",       "absent"),
    ("Ethics: causal vs correlational", "correlational, not causal",               "statistical associations",          "explicit"),
    ("Ethics: fairness",                "fairness",                                "(not expected in Ch4 prose)",       "absent"),
    ("Ethics: single institution limit", "single distance-learning institution",   "single dataset, single institution", "absent"),
    ("Class weight=None in LR",         "(not in section 3.7.3; in section 3.7.5)", "class_weight=None",                 "explicit"),
    ("LR penalty=l2",                   "(implied)",                               "L2 regularisation",                 "explicit"),
    ("LR solver=lbfgs",                 "(implied)",                               "l-bfgs solver",                     "explicit"),
    ("RF n_jobs=-1",                    "(not stated in Ch3; in Ch4)",             "n_jobs=-1",                         "explicit"),
    ("300-row SHAP subsample",          "(not in Ch3; in Ch4)",                    "300-row",                           "explicit"),
    ("Stratified subsample preserves %", "(implied)",                               "31.4 per cent Fail prevalence",     "explicit"),
    ("Withdrawn prevalence ~21%",       "(implied in Ch3)",                        "21 per cent",                       "explicit"),
    ("Random_state=42 in SMOTE",        "(implied by single fixed random seed)",   "SMOTE",                             "explicit"),
]

results = []
for label, ch3_phrase, ch4_search, expected in checks:
    in_ch3 = bool(re.search(re.escape(ch3_phrase), ch3, re.I))
    in_ch4 = bool(re.search(re.escape(ch4_search), ch4, re.I))
    results.append((label, in_ch3, in_ch4, expected))

print(f"{'STATUS':<10} {'IN Ch3':<8} {'IN Ch4':<8} {'EXPECT':<10} ITEM")
print("-" * 90)
gaps_explicit = []
gaps_mention = []
over = []
for label, in_ch3, in_ch4, expected in results:
    if expected == "explicit":
        if not in_ch4:
            status = "GAP"
            gaps_explicit.append(label)
        else:
            status = "ok"
    elif expected == "mention":
        if not in_ch4:
            status = "mention-gap"
            gaps_mention.append(label)
        else:
            status = "ok"
    elif expected == "absent":
        if in_ch4:
            status = "OVER"
            over.append(label)
        else:
            status = "ok"
    else:
        status = "?"
    print(f"{status:<10} {str(in_ch3):<8} {str(in_ch4):<8} {expected:<10} {label}")

print()
print(f"EXPLICIT GAPS (Chapter 3 mandates this in prose; Chapter 4 does not state it):")
for g in gaps_explicit:
    print(f"  - {g}")
print(f"\nMENTION GAPS (Chapter 3 references; Chapter 4 omits):")
for g in gaps_mention:
    print(f"  - {g}")
print(f"\nOVER-INCLUSIONS (Chapter 4 mentions something Chapter 3 did not sanction):")
for o in over:
    print(f"  - {o}")
