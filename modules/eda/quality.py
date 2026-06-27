from __future__ import annotations

import pandas as pd

pd.set_option("display.max_rows", 200)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("max_colwidth", None)


def constant_columns(df: pd.DataFrame) -> list[str]:
    return [column for column in df.columns if df[column].nunique(dropna=False) <= 1]


def high_cardinality_columns(
    df: pd.DataFrame,
    threshold: int = 30,
) -> pd.DataFrame:
    rows = []

    for column in df.select_dtypes(exclude="number").columns:
        unique_count = df[column].nunique(dropna=True)

        if unique_count >= threshold:
            rows.append(
                {
                    "column": column,
                    "unique_count": unique_count,
                }
            )

    return pd.DataFrame(rows)


def target_distribution(
    df: pd.DataFrame,
    target: str = "Attrition",
) -> pd.DataFrame:
    counts = df[target].value_counts(dropna=False)
    pct = df[target].value_counts(normalize=True, dropna=False) * 100

    return pd.DataFrame(
        {
            "target_value": counts.index.astype(str),
            "count": counts.values,
            "percentage": pct.round(2).values,
        }
    )
