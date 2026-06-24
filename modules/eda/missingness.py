from __future__ import annotations

import pandas as pd

pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('max_colwidth', None)


def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = pd.DataFrame(
        {
            "column": df.columns,
            "missing_count": df.isna().sum().values,
            "missing_pct": (df.isna().mean() * 100).round(2).values,
        }
    )

    return summary.sort_values(
        ["missing_pct", "missing_count"],
        ascending=False,
    ).reset_index(drop=True)


def has_missing_values(df: pd.DataFrame) -> bool:
    return bool(df.isna().sum().sum() > 0)


def shadow_matrix(df: pd.DataFrame) -> pd.DataFrame:
    return df.isna().astype(int).add_suffix("_missing")


def missingness_correlation(df: pd.DataFrame) -> pd.DataFrame:
    shadow = shadow_matrix(df)

    non_constant = shadow.loc[:, shadow.nunique() > 1]

    if non_constant.empty:
        return pd.DataFrame()

    return non_constant.corr()
