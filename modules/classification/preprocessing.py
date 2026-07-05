from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_feature_target(
    df: pd.DataFrame,
    target: str = "Attrition",
    positive_class: str = "Yes",
    drop_columns: list[str] | None = None,
) -> tuple[pd.DataFrame, pd.Series]:
    drop_columns = drop_columns or []
    columns_to_drop = [target, *[c for c in drop_columns if c in df.columns]]

    X = df.drop(columns=columns_to_drop)
    y = (df[target] == positive_class).astype(int)

    return X, y


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    numeric_columns = X.select_dtypes(include="number").columns.tolist()
    categorical_columns = X.select_dtypes(exclude="number").columns.tolist()

    return ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), numeric_columns),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_columns,
            ),
        ]
    )
