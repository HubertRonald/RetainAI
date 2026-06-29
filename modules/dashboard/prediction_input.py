from __future__ import annotations

from pathlib import Path

import pandas as pd

DEFAULT_EXCLUDED_COLUMNS = [
    "Attrition",
    "prediction",
    "attrition_probability",
    "risk_level",
]


def build_prediction_input(
    df: pd.DataFrame, excluded_columns: list[str] | None = None
) -> pd.DataFrame:
    excluded = excluded_columns or DEFAULT_EXCLUDED_COLUMNS
    return df[[c for c in df.columns if c not in excluded]].copy()


def save_prediction_sample(
    df: pd.DataFrame, output_csv: str | Path, output_xlsx: str | Path | None = None
):
    csv_path = Path(output_csv)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    xlsx_path = None
    if output_xlsx is not None:
        xlsx_path = Path(output_xlsx)
        xlsx_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(xlsx_path, index=False)
    return csv_path, xlsx_path
