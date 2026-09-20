"""Encode raw 21-feature student input into the 44-column modelling matrix.

This is the dashboard's runtime analogue of notebook 02's preprocessing:
  - ordinal mappings: age_band, imd_band
  - one-hot encoding: gender, region, highest_education, code_module
  - numeric features pass through unchanged
  - 4 derived columns mean_clicks_per_day, submission_rate,
    weighted_mean_score, mean_assessment_score are computed from inputs.

The contract is strict: the produced DataFrame has its columns in the exact
order the fitted pipelines expect (read from `X_test.parquet` at startup via
`services.feature_schema`). Any column that the training one-hot produced but
the input did not trigger is filled with 0; any value the training one-hot
never saw simply cannot be encoded here and is rejected.

This module does NOT do scaling. Scaling happens inside the LR pipeline via
`pipeline[:-1].transform(...)`. TreeSHAP for RF uses raw values.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import pandas as pd

from services import feature_schema


# Allowed categorical values (must match the training data).
GENDERS = ["F", "M"]
AGE_BANDS = ["0-35", "35-55", "55<="]
REGIONS = [
    "East Anglian Region",
    "East Midlands Region",
    "Ireland",
    "London Region",
    "North Region",
    "North Western Region",
    "Scotland",
    "South East Region",
    "South Region",
    "South West Region",
    "Wales",
    "West Midlands Region",
    "Yorkshire Region",
]
EDUCATION = [
    "A Level or Equivalent",
    "HE Qualification",
    "Lower Than A Level",
    "No Formal quals",
    "Post Graduate Qualification",
]
IMD_BANDS = [
    "0-10%", "10-20", "20-30%", "30-40%", "40-50%",
    "50-60%", "60-70%", "70-80%", "80-90%", "90-100%",
]  # missing (NaN, "?", "") maps to "Unknown"
MODULES = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG"]
PRESENTATIONS = ["2013B", "2013J", "2014B", "2014J"]


@dataclass(frozen=True)
class FormOptions:
    """All valid categorical options + numeric bounds, exposed to the form template."""
    genders: List[str]
    age_bands: List[str]
    regions: List[str]
    education: List[str]
    imd_bands: List[str]
    modules: List[str]
    presentations: List[str]


def form_options() -> FormOptions:
    return FormOptions(
        genders=GENDERS,
        age_bands=AGE_BANDS,
        regions=REGIONS,
        education=EDUCATION,
        imd_bands=IMD_BANDS,
        modules=MODULES,
        presentations=PRESENTATIONS,
    )


def age_to_code(s: str) -> int:
    """age_band string -> integer lower bound (0, 35, 55)."""
    s = str(s).strip()
    m = re.match(r"(\d+)-?", s)
    if m:
        return int(m.group(1))
    if s.startswith("55") or s.startswith("65"):
        return 55
    return 0


def imd_to_code(s: str) -> int:
    """imd_band string -> decile 0-9, or 10 for 'Unknown'."""
    s = str(s).strip()
    if s in ("", "?", "Unknown", "unknown"):
        return 10
    m = re.match(r"(\d+)-", s)
    if m:
        return int(m.group(1)) // 10
    return -1


# Number of assessments available per (module, presentation). Computed from
# the actual OULAD assessments.csv (notebook 02 uses n_distinct id_assessment).
# Note: not every (module, presentation) pair exists in OULAD; missing keys
# raise EncodingError so the user sees it explicitly.
N_ASSESSMENTS_AVAILABLE = {
    ("AAA", "2013J"): 6, ("AAA", "2014J"): 6,
    ("BBB", "2013B"): 12, ("BBB", "2013J"): 12,
    ("BBB", "2014B"): 12, ("BBB", "2014J"): 6,
    ("CCC", "2014B"): 10, ("CCC", "2014J"): 10,
    ("DDD", "2013B"): 14, ("DDD", "2013J"): 7,
    ("DDD", "2014B"): 7, ("DDD", "2014J"): 7,
    ("EEE", "2013J"): 5, ("EEE", "2014B"): 5, ("EEE", "2014J"): 5,
    ("FFF", "2013B"): 13, ("FFF", "2013J"): 13,
    ("FFF", "2014B"): 13, ("FFF", "2014J"): 13,
    ("GGG", "2013J"): 10, ("GGG", "2014B"): 10, ("GGG", "2014J"): 10,
}

# Module presentation lengths (days) per (module, presentation). Read from
# data/processed/integrated_base.parquet; they vary by presentation, not just
# by module (e.g. BBB/2013B = 240, BBB/2013J = 268, BBB/2014B = 234).
MODULE_PRESENTATION_LENGTH = {
    ("AAA", "2013J"): 268, ("AAA", "2014J"): 269,
    ("BBB", "2013B"): 240, ("BBB", "2013J"): 268,
    ("BBB", "2014B"): 234, ("BBB", "2014J"): 262,
    ("CCC", "2014B"): 241, ("CCC", "2014J"): 269,
    ("DDD", "2013B"): 240, ("DDD", "2013J"): 261,
    ("DDD", "2014B"): 241, ("DDD", "2014J"): 262,
    ("EEE", "2013J"): 268, ("EEE", "2014B"): 241, ("EEE", "2014J"): 269,
    ("FFF", "2013B"): 240, ("FFF", "2013J"): 268,
    ("FFF", "2014B"): 241, ("FFF", "2014J"): 269,
    ("GGG", "2013J"): 261, ("GGG", "2014B"): 241, ("GGG", "2014J"): 269,
}


class EncodingError(ValueError):
    pass


def _validate(features: Dict[str, Any]) -> None:
    """Raise EncodingError if any field is missing or out of range."""
    required = [
        "gender", "age_band", "region", "highest_education", "imd_band",
        "num_of_prev_attempts",
        "total_clicks", "active_days", "max_daily_clicks", "distinct_resources",
        "early_clicks_14d", "weekend_click_ratio",
        "assessments_submitted", "mean_assessment_score", "weighted_mean_score",
        "mean_days_to_submit",
        "code_module", "code_presentation",
    ]
    for k in required:
        if k not in features:
            raise EncodingError(f"Missing field: {k}")

    if features["gender"] not in GENDERS:
        raise EncodingError(f"gender must be one of {GENDERS}")
    if features["age_band"] not in AGE_BANDS:
        raise EncodingError(f"age_band must be one of {AGE_BANDS}")
    if features["region"] not in REGIONS:
        raise EncodingError(f"region must be one of {REGIONS}")
    if features["highest_education"] not in EDUCATION:
        raise EncodingError(f"highest_education must be one of {EDUCATION}")
    if features["code_module"] not in MODULES:
        raise EncodingError(f"code_module must be one of {MODULES}")
    if features["code_presentation"] not in PRESENTATIONS:
        raise EncodingError(f"code_presentation must be one of {PRESENTATIONS}")
    # Reject (module, presentation) combinations that don't exist in OULAD.
    if (features["code_module"], features["code_presentation"]) not in N_ASSESSMENTS_AVAILABLE:
        raise EncodingError(
            f"Combination code_module={features['code_module']!r}, "
            f"code_presentation={features['code_presentation']!r} does not exist in OULAD."
        )
    # IMD: empty / "?" / "Unknown" all mean "unknown"
    imd = features["imd_band"]
    if imd not in IMD_BANDS and imd not in ("", "?", "Unknown"):
        raise EncodingError(f"imd_band must be one of {IMD_BANDS} (or '?' / blank for Unknown)")

    for k in ("num_of_prev_attempts", "total_clicks", "active_days",
              "max_daily_clicks", "distinct_resources", "early_clicks_14d",
              "assessments_submitted", "mean_days_to_submit"):
        try:
            float(features[k])
        except (TypeError, ValueError):
            raise EncodingError(f"{k} must be numeric")

    for k in ("weekend_click_ratio", "mean_assessment_score", "weighted_mean_score"):
        try:
            v = float(features[k])
        except (TypeError, ValueError):
            raise EncodingError(f"{k} must be numeric")
        upper = 100 if k in ("mean_assessment_score", "weighted_mean_score") else 1
        if not (0 <= v <= upper):
            raise EncodingError(f"{k} out of range [0, {upper}]")


def encode(features: Dict[str, Any]) -> pd.DataFrame:
    """Convert 21 raw inputs into a 1 x 44 DataFrame in the training column order.

    Derived columns:
      - mean_clicks_per_day = total_clicks / active_days (0 if active_days=0)
      - submission_rate = assessments_submitted / n_assessments_available
      - weighted_mean_score = mean_assessment_score (treated as already weighted)
      - module_presentation_length = looked up from code_module
      - presentation_year = first 4 chars of code_presentation, as int
      - age_band_ord = age_to_code(age_band)
      - imd_band_ord = imd_to_code(imd_band)
    """
    _validate(features)

    total = float(features["total_clicks"])
    active = float(features["active_days"])
    mean_clicks_per_day = (total / active) if active > 0 else 0.0

    n_avail = N_ASSESSMENTS_AVAILABLE[
        (features["code_module"], features["code_presentation"])
    ]
    n_submitted = float(features["assessments_submitted"])
    submission_rate = n_submitted / n_avail if n_avail > 0 else 0.0

    # weighted_mean_score is an independent input from mean_assessment_score.
    # In OULAD it's the weighted mean of assessment scores (weight = assessment
    # weight). We accept it as its own field rather than approximating it from
    # mean_assessment_score; the round-trip test against X_test.parquet then
    # holds to floating-point precision.
    weighted_mean_score = float(features["weighted_mean_score"])

    presentation_year = int(features["code_presentation"][:4])
    module_presentation_length = MODULE_PRESENTATION_LENGTH[
        (features["code_module"], features["code_presentation"])
    ]

    # Build the one-hot vectors.
    row = {c: 0 for c in feature_schema.feature_columns()}

    # Numeric.
    row["num_of_prev_attempts"] = int(features["num_of_prev_attempts"])
    row["total_clicks"] = total
    row["active_days"] = active
    row["mean_clicks_per_day"] = mean_clicks_per_day
    row["max_daily_clicks"] = float(features["max_daily_clicks"])
    row["distinct_resources"] = float(features["distinct_resources"])
    row["early_clicks_14d"] = float(features["early_clicks_14d"])
    row["weekend_click_ratio"] = float(features["weekend_click_ratio"])
    row["assessments_submitted"] = n_submitted
    row["submission_rate"] = submission_rate
    row["mean_assessment_score"] = float(features["mean_assessment_score"])
    row["weighted_mean_score"] = weighted_mean_score
    row["mean_days_to_submit"] = float(features["mean_days_to_submit"])
    row["module_presentation_length"] = module_presentation_length
    row["presentation_year"] = presentation_year

    # Ordinal.
    row["age_band_ord"] = age_to_code(features["age_band"])
    row["imd_band_ord"] = imd_to_code(features["imd_band"])

    # One-hot: gender.
    row[f"gender_{features['gender']}"] = 1

    # One-hot: region (must match the column naming convention).
    # Region names include spaces, which are kept verbatim in column names.
    region_col = f"region_{features['region']}"
    if region_col not in row:
        # Some test-set regions may not match training; surface this clearly.
        raise EncodingError(f"region {features['region']!r} not in training one-hot vocabulary")
    row[region_col] = 1

    # One-hot: highest_education. The training prefix is "edu_" and the value
    # has spaces, e.g. "edu_A Level or Equivalent".
    edu_col = f"edu_{features['highest_education']}"
    if edu_col not in row:
        raise EncodingError(
            f"highest_education {features['highest_education']!r} not in training one-hot vocabulary"
        )
    row[edu_col] = 1

    # One-hot: code_module. The training prefix is "module_" and the value is
    # the uppercase letter code.
    module_col = f"module_{features['code_module']}"
    if module_col not in row:
        raise EncodingError(
            f"code_module {features['code_module']!r} not in training one-hot vocabulary"
        )
    row[module_col] = 1

    df = pd.DataFrame([row], columns=feature_schema.feature_columns())
    return df


def default_features_from_row(row_idx: int) -> Dict[str, Any]:
    """Reverse-engineer a 21-feature dict from a test-set row, for pre-filling the form."""
    from services import loader

    X = loader.X_test()
    if row_idx < 0 or row_idx >= len(X):
        raise IndexError(f"row_idx {row_idx} out of range")
    r = X.iloc[row_idx]

    # Find the active one-hot for each categorical by scanning columns.
    gender = "F" if int(r["gender_F"]) == 1 else "M"
    region = next(
        (c.replace("region_", "") for c in feature_schema.feature_columns()
         if c.startswith("region_") and int(r[c]) == 1),
        REGIONS[0],
    )
    edu = next(
        (c.replace("edu_", "") for c in feature_schema.feature_columns()
         if c.startswith("edu_") and int(r[c]) == 1),
        EDUCATION[0],
    )
    code_module = next(
        (c.replace("module_", "") for c in feature_schema.feature_columns()
         if c.startswith("module_") and int(r[c]) == 1),
        MODULES[0],
    )

    age_band_ord = int(r["age_band_ord"])
    age_band = {0: "0-35", 35: "35-55", 55: "55<="}.get(age_band_ord, "0-35")
    imd_band_ord = int(r["imd_band_ord"])
    imd_band = "Unknown" if imd_band_ord == 10 else IMD_BANDS[imd_band_ord]

    return {
        "gender": gender,
        "age_band": age_band,
        "region": region,
        "highest_education": edu,
        "imd_band": imd_band,
        "num_of_prev_attempts": int(r["num_of_prev_attempts"]),
        "total_clicks": float(r["total_clicks"]),
        "active_days": float(r["active_days"]),
        "max_daily_clicks": float(r["max_daily_clicks"]),
        "distinct_resources": float(r["distinct_resources"]),
        "early_clicks_14d": float(r["early_clicks_14d"]),
        "weekend_click_ratio": float(r["weekend_click_ratio"]),
        "assessments_submitted": float(r["assessments_submitted"]),
        "mean_assessment_score": float(r["mean_assessment_score"]),
        "weighted_mean_score": float(r["weighted_mean_score"]),
        "mean_days_to_submit": float(r["mean_days_to_submit"]),
        "code_module": code_module,
        "code_presentation": str(r["code_presentation"]),
    }
