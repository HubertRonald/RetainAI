import pandas as pd


def assign_risk_level(probability: float) -> str:
    if probability < 0.33:
        return "Low"
    if probability < 0.66:
        return "Medium"
    return "High"


def attach_predictions(
    df: pd.DataFrame, predictions: list[int], probabilities: list[float]
) -> pd.DataFrame:
    out = df.copy()
    out["prediction"] = predictions
    out["attrition_probability"] = probabilities
    out["risk_level"] = [assign_risk_level(p) for p in probabilities]
    return out
