from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


@dataclass
class PredictionBundle:
    input_df: pd.DataFrame
    output_df: pd.DataFrame
    required_columns: list[str]
    missing_columns: list[str]


def load_model(model_path: str | Path):
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(f"Model artifact not found: {path}")
    return joblib.load(path)


def get_model_input_columns(pipeline) -> list[str]:
    preprocessor = pipeline.named_steps.get("preprocessor")
    if preprocessor is None:
        return []

    if hasattr(preprocessor, "feature_names_in_"):
        return list(preprocessor.feature_names_in_)

    columns: list[str] = []
    for _, _, cols in getattr(preprocessor, "transformers_", []):
        if isinstance(cols, list):
            columns.extend(cols)
    return columns


def validate_prediction_input(
    df: pd.DataFrame, required_columns: list[str]
) -> list[str]:
    return [col for col in required_columns if col not in df.columns]


def risk_level(probability: float) -> str:
    if probability < 0.33:
        return "Low"
    if probability < 0.66:
        return "Medium"
    return "High"


def predict_dataframe(df: pd.DataFrame, pipeline) -> PredictionBundle:
    required_columns = get_model_input_columns(pipeline)
    missing = validate_prediction_input(df, required_columns)

    if missing:
        return PredictionBundle(
            input_df=df,
            output_df=df.copy(),
            required_columns=required_columns,
            missing_columns=missing,
        )

    X = df[required_columns].copy()
    probabilities = pipeline.predict_proba(X)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    output = df.copy()
    output["prediction"] = predictions
    output["attrition_probability"] = probabilities
    output["risk_level"] = [risk_level(float(p)) for p in probabilities]

    return PredictionBundle(
        input_df=X,
        output_df=output,
        required_columns=required_columns,
        missing_columns=[],
    )


def explain_linear_prediction(
    row_df: pd.DataFrame,
    pipeline,
    top_n: int = 12,
) -> pd.DataFrame:
    preprocessor = pipeline.named_steps.get("preprocessor")
    model = pipeline.named_steps.get("model")

    if preprocessor is None or model is None:
        return pd.DataFrame()

    if not hasattr(model, "coef_"):
        return pd.DataFrame(
            {
                "feature": ["Model explanation"],
                "contribution": [0.0],
                "direction": ["Tree/local SHAP pending"],
            }
        )

    transformed = preprocessor.transform(row_df)
    if hasattr(transformed, "toarray"):
        transformed = transformed.toarray()

    feature_names = (
        preprocessor.get_feature_names_out().tolist()
        if hasattr(preprocessor, "get_feature_names_out")
        else [f"feature_{i}" for i in range(transformed.shape[1])]
    )

    coefficients = model.coef_[0]
    contributions = transformed[0] * coefficients

    explanation = pd.DataFrame(
        {
            "feature": feature_names,
            "contribution": contributions,
            "abs_contribution": np.abs(contributions),
            "direction": np.where(contributions >= 0, "Increases risk", "Reduces risk"),
        }
    )

    return (
        explanation.sort_values("abs_contribution", ascending=False)
        .drop(columns=["abs_contribution"])
        .head(top_n)
        .reset_index(drop=True)
    )
