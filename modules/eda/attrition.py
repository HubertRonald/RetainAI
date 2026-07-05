from __future__ import annotations

import pandas as pd

pd.set_option("display.max_rows", 200)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("max_colwidth", None)


def attrition_rate_by_category(
    df: pd.DataFrame,
    column: str,
    target: str = "Attrition",
    positive_class: str = "Yes",
) -> pd.DataFrame:
    grouped = (
        df.groupby(
            column,
            dropna=False,
            observed=False,
        )[target]
        .apply(lambda values: (values == positive_class).mean() * 100)
        .reset_index(name="attrition_rate_pct")
    )

    counts = df[column].value_counts(dropna=False).reset_index()
    counts.columns = [column, "count"]

    result = grouped.merge(counts, on=column, how="left")
    return result.sort_values("attrition_rate_pct", ascending=False).reset_index(
        drop=True
    )


def attrition_rate_by_numeric_bins(
    df: pd.DataFrame,
    column: str,
    bins: int = 5,
    target: str = "Attrition",
    positive_class: str = "Yes",
) -> pd.DataFrame:
    temp = df[[column, target]].copy()
    temp[f"{column}_bin"] = pd.qcut(temp[column], q=bins, duplicates="drop")

    return attrition_rate_by_category(
        temp,
        column=f"{column}_bin",
        target=target,
        positive_class=positive_class,
    )
