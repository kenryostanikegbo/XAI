# Predicting Student Failure with Explainable Machine Learning — OULAD

This repository contains the full reproducible Jupyter-notebook pipeline for a BSc Computer Science thesis titled **"Predicting Student Failure with Explainable Machine Learning: A Comparative Study of Logistic Regression and Random Forest with SHAP Interpretability on the Open University Learning Analytics Dataset (OULAD)"**.

## What this project does

We train two binary classifiers (Logistic Regression with L2 + Random Forest) on 22,437 OULAD enrolments to predict at-risk students (Pass/Distinction = 0, Fail = 1, Withdrawn excluded). Both models are tuned with 5-fold stratified grid search on F1, wrapped in `imblearn.Pipeline` so SMOTE respects cross-validation, and explained globally + locally with SHAP.

**Headline results** (held-out test set, 6,732 rows, 31.43 % Fail prevalence):

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 0.905 | **0.898** | 0.789 | 0.840 | 0.957 |
| Random Forest | **0.914** | 0.889 | **0.831** | **0.859** | **0.962** |

**Cross-model interpretability:** Spearman ρ = 0.10 between LR and RF global feature rankings, Top-10 Jaccard = 0.25. LR leans on demographic/course-context features; RF leans on engagement metrics. The two models catch different students — see `outputs/figures/cross_model_importance.png`.

## Repository layout

```
studnetxai/
├── README.md                    # this file
├── requirements.txt             # pinned Python dependencies
├── run_nb.py                    # lightweight notebook runner (no Jupyter server needed)
├── data/
│   ├── raw/                     # OULAD CSVs (download separately, see below)
│   └── processed/               # intermediate parquet artefacts (built by the pipeline)
├── notebooks/
│   ├── 01_data_loading_and_integration.ipynb
│   ├── 02_preprocessing_and_feature_engineering.ipynb
│   ├── 03_class_imbalance_and_split.ipynb
│   ├── 04_model_training_lr_rf.ipynb
│   ├── 05_evaluation_and_metrics.ipynb
│   ├── 06_shap_global_interpretability.ipynb
│   ├── 07_shap_local_interpretability.ipynb
│   └── 08_cross_model_comparison.ipynb
└── outputs/
    ├── figures/                 # 21 PNG figures for Chapter 4
    ├── tables/                  # 13 CSV tables for Chapter 4
    └── models/                  # 5 trained estimators + SHAP arrays + explainers
```

## Reproducibility

All code paths use `random_state=42` (split, CV shuffle, SMOTE, RF init). Re-running all eight notebooks on a clean clone produces identical metrics to within floating-point precision.

### Quick start

```bash
# 1. Create a project-local virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# 2. Install pinned dependencies
pip install -r requirements.txt

# 3. Download the OULAD dataset into data/raw/  (see below for sources)

# 4. Run the pipeline
python run_nb.py notebooks/01_data_loading_and_integration.ipynb
python run_nb.py notebooks/02_preprocessing_and_feature_engineering.ipynb
python run_nb.py notebooks/03_class_imbalance_and_split.ipynb
python run_nb.py notebooks/04_model_training_lr_rf.ipynb
python run_nb.py notebooks/05_evaluation_and_metrics.ipynb
python run_nb.py notebooks/06_shap_global_interpretability.ipynb
python run_nb.py notebooks/07_shap_local_interpretability.ipynb
python run_nb.py notebooks/08_cross_model_comparison.ipynb
```

Each notebook writes its outputs into `data/processed/` or `outputs/` and can be re-run safely.

### Expected runtimes (Windows 11, Python 3.11, single machine)

| Notebook | Time |
|---|---|
| 01_data_loading_and_integration | ~30 s |
| 02_preprocessing_and_feature_engineering | ~10 s |
| 03_class_imbalance_and_split | <5 s |
| 04_model_training_lr_rf | ~30 s (LR + RF grid search) |
| 05_evaluation_and_metrics | <5 s |
| 06_shap_global_interpretability | ~2-3 min (TreeSHAP on 500-tree RF) |
| 07_shap_local_interpretability | ~30 s |
| 08_cross_model_comparison | <10 s |
| **Total** | **~5 min** |

### Dataset — where to get OULAD

The Open University Learning Analytics Dataset (Kuzilek, Hlosta, Zdrahal, 2017) contains 7 CSV tables totalling ~470 MB. It is openly licensed (CC-BY 4.0). Three reliable download sources:

1. **UCI Machine Learning Repository** — <https://archive.ics.uci.edu/ml/datasets/Open+University+Learning+Analytics+dataset>
2. **Open University's own mirror** — <http://www.openuniversity.edu>
3. **Kaggle mirror** — search "OULAD" (community-uploaded, convenience)

Place the seven CSVs into `data/raw/`:
```
studentInfo.csv          studentRegistration.csv
studentVle.csv           vle.csv
studentAssessment.csv    courses.csv
assessments.csv
```

### Sanity check after a fresh clone

After running notebooks 01–08, the following files should exist:

- `outputs/tables/metrics_comparison.csv` — exact rows: see §4.x
- `outputs/figures/roc_curves.png`, `pr_curves.png`
- `outputs/figures/shap_summary_lr.png`, `shap_summary_rf.png`
- `outputs/figures/shap_local_{tp,tn,fp,fn,borderline-1,borderline-2}_{lr,rf}.png` (12 plots)
- `outputs/figures/cross_model_importance.png`, `cross_model_scatter.png`
- `outputs/tables/cross_model_summary.csv` — `spearman_rho ≈ 0.10`, `top10_jaccard ≈ 0.25`

## Methodology highlights

(Full detail in Chapters 3–4.)

- **Class imbalance:** Fail = 31.4 % of retained enrolments → moderate imbalance. SMOTE only, no `class_weight` appendix (per §3.7.1 mild-imbalance branch).
- **No leakage:** SMOTE lives inside `imblearn.pipeline.Pipeline` so cross-validation refits it on each training fold. StandardScaler likewise. Test set is touched exactly once (notebook 05).
- **Feature engineering:** 21 features in 4 groups (Demographics, VLE engagement, Assessment, Course context) — Table 3.1. One-hot expansion → 44 modelling features.
- **Tuning:** `GridSearchCV(scoring='f1', cv=StratifiedKFold(5))` on each model.
- **Interpretability:** LinearSHAP for LR (log-odds scale), TreeSHAP for RF (probability scale). 6 illustrative local cases (TP, TN, FP, FN, 2 borderline). Spearman ρ + Top-10 Jaccard for cross-model agreement.

## Software environment

Pinned in `requirements.txt`:
```
pandas==2.2.3          numpy==1.26.4         matplotlib==3.9.2
seaborn==0.13.2        scikit-learn==1.5.2   imbalanced-learn==0.12.4
shap==0.46.0           jupyter==1.1.1        ipykernel==6.29.5
pyarrow==17.0.0
```

Python 3.11 tested. Python 3.10+ should also work.

## Citation

If you build on this work, please cite both the dataset and the methodology:

- Kuzilek, J., Hlosta, M., & Zdrahal, Z. (2017). *Open University Learning Analytics dataset*. Scientific Data, 4:170171. <https://doi.org/10.1038/sdata.2017.171>
- Lundberg, S. M., & Lee, S.-I. (2017). *A unified approach to interpreting model predictions*. NeurIPS 2017.
- Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., & Lee, S.-I. (2020). *From local explanations to global understanding with explainable AI for trees*. Nature Machine Intelligence, 2(1), 56-67.
