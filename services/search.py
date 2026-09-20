"""Search the 300-row stratified SHAP subset by id_student for the picker.

We deliberately limit the picker to the 300 rows in `shap_indices_strat.npy` —
the same subset for which the dissertation pre-cached RF SHAP and pre-rendered
waterfalls. Picking a row from this subset gives the tutor both classifiers'
SHAP waterfalls immediately, which is what makes the picker useful (otherwise
RF SHAP would be unavailable and the picker would be a slower way to get the
same LR-only result as the live form).
"""
from __future__ import annotations

from functools import lru_cache
from typing import Dict, List

import numpy as np
import pandas as pd

from services import loader

_CACHED: pd.DataFrame | None = None


def _build() -> pd.DataFrame:
    """Build the searchable index over the 300-row stratified subset."""
    from services import predictor

    X = loader.X_test()
    y = loader.y_test()
    shap_indices = loader.shap_indices()
    df = X.iloc[shap_indices].copy()
    df = df.reset_index(drop=False).rename(columns={"index": "row_idx"})
    df["row_idx"] = df["row_idx"].astype(int)
    df["id_student"] = df["id_student"].astype(int)
    df["code_presentation"] = df["code_presentation"].astype(str)
    # Pick the active module one-hot column. Must match the prefix exactly,
    # not "contains" — `module_presentation_length` is also a column and
    # `.filter(like="module_")` would include it, breaking the idxmax.
    module_cols = [c for c in df.columns if c.startswith("module_") and c != "module_presentation_length"]
    df["code_module"] = df[module_cols].idxmax(axis=1).str.replace("module_", "", regex=False)
    df["y_true"] = y.iloc[shap_indices].astype(int).to_numpy()

    # Pre-compute predictions (300 calls; ~1s)
    lr_p = np.empty(len(df), dtype=float)
    rf_p = np.empty(len(df), dtype=float)
    for i in range(len(df)):
        r = predictor.predict_one(int(df["row_idx"].iloc[i]))
        lr_p[i] = r.lr_proba
        rf_p[i] = r.rf_proba
    df["lr_proba"] = lr_p
    df["rf_proba"] = rf_p
    return df


@lru_cache(maxsize=1)
def search_index() -> pd.DataFrame:
    """Return (and cache) the 300-row search index. Built once per process."""
    global _CACHED
    if _CACHED is None:
        _CACHED = _build()
    return _CACHED


def search(query: str, limit: int = 20) -> List[Dict]:
    """Return at most `limit` rows whose id_student contains `query`.

    If `query` is empty, returns the first `limit` rows (so the picker has
    something to show on first focus).
    Results are sorted by id_student ascending.
    """
    df = search_index()
    if query:
        mask = df["id_student"].astype(str).str.contains(query, regex=False)
        hits = df[mask]
    else:
        hits = df
    hits = hits.sort_values("id_student", kind="stable").head(limit)
    return [
        {
            "row_idx": int(r.row_idx),
            "id_student": int(r.id_student),
            "code_presentation": str(r.code_presentation),
            "code_module": str(r.code_module),
            "y_true": int(r.y_true),
            "lr_proba": round(float(r.lr_proba), 4),
            "rf_proba": round(float(r.rf_proba), 4),
        }
        for r in hits.itertuples(index=False)
    ]

