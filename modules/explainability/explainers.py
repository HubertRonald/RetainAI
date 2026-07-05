from __future__ import annotations

import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


def build_shap_explainer(model, background):
    model_name = model.__class__.__name__.lower()

    if isinstance(model, LogisticRegression):
        return shap.LinearExplainer(model, background)

    if isinstance(model, RandomForestClassifier) or "xgb" in model_name:
        return shap.TreeExplainer(model)

    return shap.Explainer(model, background)
