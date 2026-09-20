"""Predict and explain with both classifiers, honouring the LR/RF input-space split.

INPUT-SPACE ASYMMETRY (most likely silent-failure mode)
-------------------------------------------------------
- LR pipeline: [SMOTE, StandardScaler, LogisticRegression]. The fitted
  LinearExplainer was trained on the *post-scaler* output, so LR SHAP values
  come in log-odds units on the standardised feature space. We must therefore
  pass `scaler.transform(X)` into the explainer, not raw X.

- RF pipeline: [SMOTE, RandomForest]. TreeSHAP is defined on the raw feature
  values (the tree was fit on raw inputs), and returns probability-space SHAP
  values. We pass raw X into the RF explainer.

Magnitudes are NOT comparable across the two (log-odds vs probability), but
*signs* and *ranks* are. That is the cross-model comparison the dissertation
makes.

WHY LIVE SHAP, NOT THE CACHED ARRAYS
-------------------------------------
We have a cached `shap_values_lr.npy` (6732 x 44) and a cached `shap_values_rf.npy`
(300 x 44). We use them only for the RF explainer shortcut (only 300 rows have a
cached array; computing live TreeSHAP on ad-hoc rows would be slow). For LR we
compute SHAP live because the cached array turned out to be inconsistent with
the dissertation's reported local SHAP values in Chapter 4 §4.7 — the live
LinearExplainer matches the narratives the user reads in the dissertation.
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import Any, Dict, Optional

import numpy as np

from services import encoder, loader

# imblearn's SMOTE step strips pandas feature names, which makes sklearn emit a
# UserWarning on every predict_proba call. The warning is not actionable (the
# prediction is correct; SMOTE only resamples during fit, not predict) so we
# silence it at module load.
warnings.filterwarnings(
    "ignore",
    message="X does not have valid feature names",
    category=UserWarning,
)


@dataclass(frozen=True)
class PredictionResult:
    lr_proba: float
    rf_proba: float
    lr_pred: int
    rf_pred: int
    y_true: int


@dataclass(frozen=True)
class ExplanationResult:
    lr_shap: list  # length-44 list of floats (log-odds)
    rf_shap: Optional[list]  # length-44 list of floats (probability) or None


@dataclass(frozen=True)
class LivePredictionResult:
    """Same shape as PredictionResult + ExplanationResult for ad-hoc input."""
    lr_proba: float
    rf_proba: float
    lr_pred: int
    rf_pred: int
    lr_shap: list  # length-44 list of floats (log-odds)
    rf_shap: Optional[list]  # length-44 list of floats (probability) or None
    feature_names: list  # length-44 list of feature column names


def _validate_row_idx(row_idx: int) -> None:
    X = loader.X_test()
    if row_idx < 0 or row_idx >= len(X):
        raise IndexError(
            f"row_idx {row_idx} out of range; X_test has {len(X)} rows"
        )


def _row_values(row_idx: int) -> np.ndarray:
    X = loader.X_test()
    return X.iloc[[row_idx]].drop(columns=["id_student", "code_presentation"]).values


def _row_dataframe(row_idx: int):
    """Return the row as a DataFrame with feature names (sklearn complains otherwise)."""
    import pandas as pd
    from services.feature_schema import feature_columns

    X = loader.X_test()
    row = X.iloc[[row_idx]].drop(columns=["id_student", "code_presentation"])
    # Reorder to the canonical training column order, in case X_test has drifted.
    return pd.DataFrame(row.values, columns=list(feature_columns()))


def predict_one(row_idx: int) -> PredictionResult:
    """Return both classifiers' predictions and the true label for one test row."""
    _validate_row_idx(row_idx)
    y = loader.y_test()
    df = _row_dataframe(row_idx)

    lr_proba = float(loader.lr_pipeline().predict_proba(df)[0, 1])
    rf_proba = float(loader.rf_pipeline().predict_proba(df)[0, 1])

    return PredictionResult(
        lr_proba=lr_proba,
        rf_proba=rf_proba,
        lr_pred=int(lr_proba >= 0.5),
        rf_pred=int(rf_proba >= 0.5),
        y_true=int(y.iloc[row_idx]),
    )


def explain_one(row_idx: int) -> ExplanationResult:
    """Return SHAP values for both classifiers for one test row.

    LR SHAP is computed live (the cached array is inconsistent with the
    dissertation's local SHAP narratives in Chapter 4 §4.7; live computation
    matches the numbers the dissertation reports).

    RF SHAP is pulled from the cached 300-row subsample array when row_idx is
    inside that subset; otherwise the live TreeSHAP would be too expensive to
    run on demand, so we report None and the UI shows the fallback message.
    """
    _validate_row_idx(row_idx)
    df = _row_dataframe(row_idx)
    rv = df.values

    # LR: live compute against the live explainer.
    scaler = loader.lr_pipeline().named_steps["scaler"]
    row_scaled = scaler.transform(rv)
    lr_sv = loader.lr_explainer().shap_values(row_scaled)
    lr_shap = np.asarray(lr_sv).reshape(-1).tolist()
    if len(lr_shap) != 44:
        raise RuntimeError(
            f"LR SHAP returned shape {np.asarray(lr_sv).shape}; expected (1, 44) or (44,)"
        )

    # RF: pull from cached 300-row array if available, else None.
    shap_indices = loader.shap_indices()
    rf_shap: Optional[list] = None
    matches = np.where(shap_indices == row_idx)[0]
    if len(matches):
        subset_pos = int(matches[0])
        rf_shap = loader.shap_rf()[subset_pos].tolist()

    return ExplanationResult(lr_shap=lr_shap, rf_shap=rf_shap)


def shap_subset_position_for(row_idx: int) -> Optional[int]:
    """Return the position of row_idx within the 300-row SHAP subset, or None."""
    shap_indices = loader.shap_indices()
    matches = np.where(shap_indices == row_idx)[0]
    return int(matches[0]) if len(matches) else None


def rf_shap_for_features(features: Dict[str, Any]) -> Optional[list]:
    """Compute TreeSHAP for an ad-hoc 21-feature input.

    This is intentionally separate from predict_and_explain_from_features so
    the dashboard can run it asynchronously after the LR result is already on
    screen. Returns the length-44 list of float SHAP values in probability
    space, or raises on failure.
    """
    df = encoder.encode(features)
    rv = df.values
    rf_sv = loader.rf_explainer().shap_values(rv)
    # rf_explainer may return a list of two arrays (class 0, class 1) under
    # older shap versions, or a 3-D array under newer ones. The failure class
    # is index 1.
    arr = np.asarray(rf_sv)
    if arr.ndim == 3:
        arr = arr[0, :, 1]   # newer shap: shape (1, n_features, n_classes)
    elif isinstance(rf_sv, list) and len(rf_sv) == 2:
        arr = np.asarray(rf_sv[1])[0]  # older shap: [class0, class1]
    arr = np.asarray(arr).reshape(-1)
    if arr.shape[0] != 44:
        raise RuntimeError(
            f"RF SHAP returned shape {arr.shape}; expected (44,)"
        )
    return arr.tolist()


# ---- Live input path -----------------------------------------------------

def predict_and_explain_from_features(features: Dict[str, Any]) -> LivePredictionResult:
    """Predict and explain for an ad-hoc 21-feature student input.

    Both classifiers receive the same encoded DataFrame (21 inputs -> 44 columns
    in the training column order, then no further scaling — the LR pipeline
    owns its own StandardScaler step, the RF pipeline operates on raw values).

    Both LR and RF SHAP are computed inline. Empirically TreeSHAP on a single
    ad-hoc row takes ~300 ms for 500 trees × 44 features, well within the
    user's tolerance for a Predict click.
    """
    from services.feature_schema import feature_columns

    df = encoder.encode(features)
    rv = df.values

    lr_proba = float(loader.lr_pipeline().predict_proba(df)[0, 1])
    rf_proba = float(loader.rf_pipeline().predict_proba(df)[0, 1])

    scaler = loader.lr_pipeline().named_steps["scaler"]
    row_scaled = scaler.transform(rv)
    lr_sv = loader.lr_explainer().shap_values(row_scaled)
    lr_shap = np.asarray(lr_sv).reshape(-1).tolist()
    if len(lr_shap) != 44:
        raise RuntimeError(
            f"LR SHAP returned shape {np.asarray(lr_sv).shape}; expected (1, 44) or (44,)"
        )

    rf_shap = rf_shap_for_features(features)

    return LivePredictionResult(
        lr_proba=lr_proba,
        rf_proba=rf_proba,
        lr_pred=int(lr_proba >= 0.5),
        rf_pred=int(rf_proba >= 0.5),
        lr_shap=lr_shap,
        rf_shap=rf_shap,
        feature_names=list(feature_columns()),
    )


# ---- Self-tests ----------------------------------------------------------

def _self_test_lr_shap_matches_cache() -> None:
    """Verify live LR SHAP equals the cached array at a known canonical case.

    The cached shap_values_lr.npy was generated by the same LinearExplainer on
    the same X_test_feat in notebook 06. We compare the live computation for
    the TP case's X_test row against the cached entry at the corresponding
    position; they should agree to floating-point precision.

    The TP case lives in `shap_indices_strat[2]` (X_test row 2945), per
    outputs/tables/local_cases.csv (subset_pos=2).
    """
    X = loader.X_test()
    shap_indices = loader.shap_indices()
    tp_subset_pos = 2  # canonical TP case
    row_idx = int(shap_indices[tp_subset_pos])

    explanation = explain_one(row_idx)
    cached = loader.shap_lr()[row_idx]

    diff = max(abs(c - k) for c, k in zip(explanation.lr_shap, cached))
    if diff > 1e-9:
        raise RuntimeError(
            f"LR SHAP self-test failed at TP (row_idx={row_idx}): "
            f"max |live - cached| = {diff:.3e}. Check that explain_one is "
            "calling scaler.transform() before shap_values()."
        )


def _self_test_lr_shap_matches_narrative() -> None:
    """Cross-check: live LR SHAP for TP matches the dissertation narrative.

    Chapter 4 §4.7 reports `submission_rate SHAP = +6.730` as the top
    contribution for the TP case under LR. This test ensures the numbers the
    dashboard serves are the numbers the dissertation reports.
    """
    from services.feature_schema import feature_columns

    shap_indices = loader.shap_indices()
    row_idx = int(shap_indices[2])  # TP subset_pos = 2

    explanation = explain_one(row_idx)
    feats = list(feature_columns())
    sr_idx = feats.index("submission_rate")
    sr_shap = explanation.lr_shap[sr_idx]

    if not (5.0 < sr_shap < 8.5):
        raise RuntimeError(
            f"LR SHAP narrative check failed: submission_rate SHAP = "
            f"{sr_shap:.3f}, expected ~+6.730 per dissertation narrative. "
            "Check that explain_one is calling scaler.transform() before "
            "shap_values()."
        )


def run_self_tests() -> None:
    """Call from app startup. Raises if any check fails."""
    loader.warm()
    _self_test_lr_shap_matches_cache()
    _self_test_lr_shap_matches_narrative()
