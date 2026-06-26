from __future__ import annotations

import pandas as pd


def prepare_survival_dataset(
        df: pd.DataFrame,
        duration_col: str = "YearsAtCompany",
        event_col: str = "Attrition",
        positive_class: str = "Yes",
        drop_columns: list[str] | None = None,
    ) -> pd.DataFrame:
    drop_columns = drop_columns or []

    survival_df = df.copy()
    survival_df["duration"] = survival_df[duration_col].astype(float)
    survival_df["event"] = (survival_df[event_col] == positive_class).astype(int)

    # Lifelines handles duration values, but a tiny offset avoids edge-case issues
    # for employees with zero years at company.
    survival_df["duration"] = survival_df["duration"].clip(lower=0.01)

    columns_to_drop = [event_col, *[c for c in drop_columns if c in survival_df.columns]]
    survival_df = survival_df.drop(columns=columns_to_drop)

    return survival_df


def prepare_cox_features(
        survival_df: pd.DataFrame,
        duration_col: str = "duration",
        event_col: str = "event",
    ) -> pd.DataFrame:
    base_cols = [duration_col, event_col]

    X = survival_df.drop(columns=base_cols)
    X = pd.get_dummies(X, drop_first=True)

    cox_df = pd.concat([survival_df[base_cols], X], axis=1)

    # Remove constant columns to reduce Cox convergence issues.
    constant_columns = [
        col for col in cox_df.columns
        if col not in base_cols and cox_df[col].nunique(dropna=False) <= 1
    ]

    if constant_columns:
        cox_df = cox_df.drop(columns=constant_columns)

    return cox_df
