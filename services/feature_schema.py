"""Single source of truth for the 44 modelling-feature column order.

The order is read from `data/processed/split/X_test.parquet` at first access and
frozen. This is the column order the fitted pipelines expect, so any caller that
needs to build an input row must follow it exactly.

X_test.parquet has 46 columns: 44 features + id_student + code_presentation (keys).
We drop the two keys and expose the remaining 44.
"""
from __future__ import annotations

from functools import lru_cache
from typing import List

from services import loader

KEY_COLUMNS = ("id_student", "code_presentation")


@lru_cache(maxsize=1)
def feature_columns() -> List[str]:
    """Return the frozen 44-feature column order."""
    cols = list(loader.X_test().columns)
    feature_cols = [c for c in cols if c not in KEY_COLUMNS]
    if len(feature_cols) != 44:
        raise RuntimeError(
            f"Expected 44 feature columns in X_test.parquet, found {len(feature_cols)}. "
            "Has the preprocessing pipeline changed?"
        )
    return tuple(feature_cols)  # tuple to be hashable for lru_cache


def n_features() -> int:
    return len(feature_columns())
