"""Local-case lookup: load the 6 canonical cases (TP/TN/FP/FN/borderline-1/2) and
join them with their narrative markdown.

The two source CSVs are:
  - outputs/tables/local_cases.csv         (case, id_student, code_presentation,
                                            y_true, lr_pred, rf_pred, lr_proba,
                                            rf_proba, subset_pos)
  - outputs/tables/local_case_narratives.csv (case, model, narrative_markdown)

We also resolve the X_test row_idx for each case at startup so the dashboard can
deep-link from /local-cases to /student/<row_idx>.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict, List

import pandas as pd

from services import loader

TABLES_DIR = Path(__file__).resolve().parent.parent / "outputs" / "tables"


@dataclass(frozen=True)
class LocalCase:
    case: str
    row_idx: int
    subset_pos: int
    id_student: int
    code_presentation: str
    y_true: int
    lr_pred: int
    rf_pred: int
    lr_proba: float
    rf_proba: float
    lr_narrative: str
    rf_narrative: str

    @property
    def model_disagreement(self) -> bool:
        return self.lr_pred != self.rf_pred


@lru_cache(maxsize=1)
def all_cases() -> Dict[str, LocalCase]:
    """Load and join the local_cases and local_case_narratives CSVs once."""
    loader.warm()  # ensures X_test is available
    cases_df = pd.read_csv(TABLES_DIR / "local_cases.csv")
    narratives_df = pd.read_csv(TABLES_DIR / "local_case_narratives.csv")

    X = loader.X_test()

    out: Dict[str, LocalCase] = {}
    for _, row in cases_df.iterrows():
        mask = (
            (X["id_student"].astype(str) == str(int(row["id_student"])))
            & (X["code_presentation"].astype(str) == str(row["code_presentation"]))
        )
        if not mask.any():
            raise RuntimeError(
                f"Local case {row['case']} (id_student={row['id_student']}, "
                f"code_presentation={row['code_presentation']}) not found in "
                "X_test.parquet"
            )
        row_idx = int(mask.values.argmax())

        lr_nar = narratives_df[
            (narratives_df["case"] == row["case"]) & (narratives_df["model"] == "LR")
        ]["narrative"].iloc[0]
        rf_nar = narratives_df[
            (narratives_df["case"] == row["case"]) & (narratives_df["model"] == "RF")
        ]["narrative"].iloc[0]

        out[row["case"]] = LocalCase(
            case=row["case"],
            row_idx=row_idx,
            subset_pos=int(row["subset_pos"]),
            id_student=int(row["id_student"]),
            code_presentation=str(row["code_presentation"]),
            y_true=int(row["y_true"]),
            lr_pred=int(row["lr_pred"]),
            rf_pred=int(row["rf_pred"]),
            lr_proba=float(row["lr_proba"]),
            rf_proba=float(row["rf_proba"]),
            lr_narrative=lr_nar,
            rf_narrative=rf_nar,
        )
    return out


def list_cases() -> List[LocalCase]:
    """Return the 6 cases in display order."""
    order = ["TP", "TN", "FP", "FN", "Borderline-1", "Borderline-2"]
    cases = all_cases()
    return [cases[c] for c in order if c in cases]


def get_case(case: str) -> LocalCase:
    cases = all_cases()
    if case not in cases:
        raise KeyError(f"Unknown case {case!r}")
    return cases[case]


def get_case_by_row_idx(row_idx: int) -> LocalCase:
    """Return the canonical case whose X_test row index matches row_idx, or raise KeyError."""
    for c in all_cases().values():
        if c.row_idx == row_idx:
            return c
    raise KeyError(f"No canonical case has row_idx={row_idx}")
