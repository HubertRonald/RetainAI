from __future__ import annotations

import pandas as pd

pd.set_option("display.max_rows", 200)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("max_colwidth", None)


def numeric_correlation_matrix(
    df: pd.DataFrame,
    method: str = "pearson",
) -> pd.DataFrame:
    numeric_df = df.select_dtypes(include="number")
    return numeric_df.corr(method=method)


def target_numeric_correlation(
    df: pd.DataFrame,
    target: str = "Attrition",
    positive_class: str = "Yes",
    method: str = "pearson",
) -> pd.DataFrame:
    temp = df.copy()
    temp[f"{target}_binary"] = (temp[target] == positive_class).astype(int)

    correlations = (
        temp.select_dtypes(include="number")
        .corr(method=method)[f"{target}_binary"]
        .drop(f"{target}_binary")
        .sort_values(key=lambda values: values.abs(), ascending=False)
    )

    return correlations.reset_index().rename(
        columns={"index": "feature", f"{target}_binary": "correlation"}
    )
