"""Singleton loader for fitted models, SHAP explainers, cached SHAP arrays, and X_test.

Total resident memory after warm() is approximately 250 MB:
  - lr_best.joblib ............. 1.7 MB
  - rf_best.joblib ............. 89 MB
  - shap_explainer_lr.joblib ... 74 KB
  - shap_explainer_rf.joblib ... 117 MB
  - shap_values_lr.npy ......... 2.4 MB (6732 x 44 float64)
  - shap_values_rf.npy ......... 105 KB (300 x 44 float64)
  - shap_indices_strat.npy ..... 1.3 KB
  - X_test.parquet ............. ~3 MB (6732 x 46)
  - y_test.parquet ............. ~2 KB

warm() is idempotent. The dashboard uses 1 gunicorn worker because of this footprint;
see DEPLOY.md for cloud-tier sizing notes.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import joblib
import numpy as np
import pandas as pd

# Project root is one level up from this file (services/loader.py -> studnetxai/).
PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODELS_DIR = PROJECT_ROOT / "outputs" / "models"
DATA_DIR = PROJECT_ROOT / "data" / "processed" / "split"

# Module-level singletons. Populated by warm().
_lr_pipeline = None
_rf_pipeline = None
_lr_explainer = None
_rf_explainer = None
_shap_lr: Optional[np.ndarray] = None  # shape (6732, 44)
_shap_rf: Optional[np.ndarray] = None  # shape (300, 44)
_shap_indices: Optional[np.ndarray] = None  # shape (300,) row indices into X_test
_X_test: Optional[pd.DataFrame] = None  # columns = [44 features, id_student, code_presentation]
_y_test: Optional[pd.Series] = None  # binary 0/1, index-aligned with X_test
_test_predictions: Optional[pd.DataFrame] = None  # 6732 rows, from test_predictions.csv


def warm() -> None:
    """Load all artifacts into module-level singletons. Idempotent."""
    global _lr_pipeline, _rf_pipeline, _lr_explainer, _rf_explainer
    global _shap_lr, _shap_rf, _shap_indices
    global _X_test, _y_test, _test_predictions

    if _lr_pipeline is not None:
        return  # already warmed

    _lr_pipeline = joblib.load(MODELS_DIR / "lr_best.joblib")
    _rf_pipeline = joblib.load(MODELS_DIR / "rf_best.joblib")
    _lr_explainer = joblib.load(MODELS_DIR / "shap_explainer_lr.joblib")
    _rf_explainer = joblib.load(MODELS_DIR / "shap_explainer_rf.joblib")

    _shap_lr = np.load(MODELS_DIR / "shap_values_lr.npy")
    _shap_rf = np.load(MODELS_DIR / "shap_values_rf.npy")
    _shap_indices = np.load(MODELS_DIR / "shap_indices_strat.npy")

    _X_test = pd.read_parquet(DATA_DIR / "X_test.parquet")
    _y_test = pd.read_parquet(DATA_DIR / "y_test.parquet")["y"]

    _test_predictions = pd.read_csv(MODELS_DIR / "test_predictions.csv")


# Accessors. Use these instead of touching globals directly so static analysers can
# tell when something is uninitialised.

def lr_pipeline():
    warm()
    return _lr_pipeline


def rf_pipeline():
    warm()
    return _rf_pipeline


def lr_explainer():
    warm()
    return _lr_explainer


def rf_explainer():
    warm()
    return _rf_explainer


def shap_lr() -> np.ndarray:
    warm()
    return _shap_lr


def shap_rf() -> np.ndarray:
    warm()
    return _shap_rf


def shap_indices() -> np.ndarray:
    warm()
    return _shap_indices


def X_test() -> pd.DataFrame:
    warm()
    return _X_test


def y_test() -> pd.Series:
    warm()
    return _y_test


def test_predictions() -> pd.DataFrame:
    warm()
    return _test_predictions


def is_warmed() -> bool:
    return _lr_pipeline is not None
