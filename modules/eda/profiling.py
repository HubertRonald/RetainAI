from __future__ import annotations

import pandas as pd

pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('max_colwidth', None)

def dataset_overview(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "metric": ["rows", "columns", "duplicated_rows"],
            "value": [df.shape[0], df.shape[1], int(df.duplicated().sum())],
        }
    )


def column_profile(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "column": df.columns,
            "dtype": [str(dtype) for dtype in df.dtypes],
            "non_null_count": df.notna().sum().values,
            "null_count": df.isna().sum().values,
            "null_pct": (df.isna().mean() * 100).round(2).values,
            "unique_count": df.nunique(dropna=True).values,
        }
    )


def numeric_profile(df: pd.DataFrame) -> pd.DataFrame:
    return df.select_dtypes(include="number").describe().T.reset_index(names="column")


def categorical_profile(df: pd.DataFrame) -> pd.DataFrame:
    categorical = df.select_dtypes(exclude="number")
    rows = []

    for column in categorical.columns:
        rows.append(
            {
                "column": column,
                "unique_count": categorical[column].nunique(dropna=True),
                "top_value": categorical[column].mode(dropna=True).iloc[0]
                if not categorical[column].mode(dropna=True).empty
                else None,
                "top_frequency": categorical[column].value_counts(dropna=True).iloc[0]
                if not categorical[column].value_counts(dropna=True).empty
                else 0,
            }
        )

    return pd.DataFrame(rows)
