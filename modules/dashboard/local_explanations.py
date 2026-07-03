from __future__ import annotations

import numpy as np
import pandas as pd


def _to_dense(matrix):
    if hasattr(matrix, "toarray"):
        return matrix.toarray()
    return matrix


def _feature_names(preprocessor, n_features: int) -> list[str]:
    if hasattr(preprocessor, "get_feature_names_out"):
        return preprocessor.get_feature_names_out().tolist()
    return [f"feature_{idx}" for idx in range(n_features)]


def _positive_class_values(values):
    if isinstance(values, list):
        return values[1] if len(values) > 1 else values[0]

    if isinstance(values, tuple):
        return values[1] if len(values) > 1 else values[0]

    arr = np.asarray(values)

    if arr.ndim == 3:
        return arr[:, :, 1] if arr.shape[-1] > 1 else arr[:, :, 0]

    return arr


def _linear_contributions(row_df: pd.DataFrame, pipeline, top_n: int) -> pd.DataFrame:
    preprocessor = pipeline.named_steps.get("preprocessor")
    model = pipeline.named_steps.get("model")

    transformed = _to_dense(preprocessor.transform(row_df))
    names = _feature_names(preprocessor, transformed.shape[1])

    coefficients = model.coef_[0]
    contributions = transformed[0] * coefficients

    explanation = pd.DataFrame(
        {
            "feature": names,
            "contribution": contributions,
            "abs_contribution": np.abs(contributions),
            "direction": np.where(contributions >= 0, "Increases risk", "Reduces risk"),
            "explanation_type": "linear_contribution",
        }
    )

    return (
        explanation.sort_values("abs_contribution", ascending=False)
        .drop(columns=["abs_contribution"])
        .head(top_n)
        .reset_index(drop=True)
    )


def _tree_shap_contributions(
    row_df: pd.DataFrame,
    pipeline,
    background_df: pd.DataFrame | None,
    top_n: int,
) -> pd.DataFrame:
    try:
        import shap
    except ImportError as exc:
        raise ImportError(
            "SHAP is required for tree row-level explanations. "
            "Install retainai[explainability]."
        ) from exc

    preprocessor = pipeline.named_steps.get("preprocessor")
    model = pipeline.named_steps.get("model")

    row_matrix = _to_dense(preprocessor.transform(row_df))
    names = _feature_names(preprocessor, row_matrix.shape[1])

    if background_df is not None and len(background_df) > 0:
        background_matrix = _to_dense(preprocessor.transform(background_df))
        background_matrix = background_matrix[: min(len(background_matrix), 100)]
        explainer = shap.TreeExplainer(model, data=background_matrix)
    else:
        explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(row_matrix)
    selected = _positive_class_values(shap_values)

    selected = np.asarray(selected)
    if selected.ndim == 2:
        contributions = selected[0]
    else:
        contributions = selected

    explanation = pd.DataFrame(
        {
            "feature": names,
            "contribution": contributions,
            "abs_contribution": np.abs(contributions),
            "direction": np.where(contributions >= 0, "Increases risk", "Reduces risk"),
            "explanation_type": "tree_shap",
        }
    )

    return (
        explanation.sort_values("abs_contribution", ascending=False)
        .drop(columns=["abs_contribution"])
        .head(top_n)
        .reset_index(drop=True)
    )


def explain_prediction_row(
    row_df: pd.DataFrame,
    pipeline,
    background_df: pd.DataFrame | None = None,
    top_n: int = 12,
) -> pd.DataFrame:
    preprocessor = pipeline.named_steps.get("preprocessor")
    model = pipeline.named_steps.get("model")

    if preprocessor is None or model is None:
        return pd.DataFrame()

    if hasattr(model, "coef_"):
        return _linear_contributions(row_df=row_df, pipeline=pipeline, top_n=top_n)

    return _tree_shap_contributions(
        row_df=row_df,
        pipeline=pipeline,
        background_df=background_df,
        top_n=top_n,
    )
