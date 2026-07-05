from __future__ import annotations

import numpy as np

from modules.explainability.feature_importance import shap_feature_importance
from modules.explainability.shap_values import get_expected_value


class DummyExplainer:
    expected_value = [0.1, 0.9]


def test_shap_feature_importance() -> None:
    shap_values = np.array([[0.1, -0.2, 0.3], [0.2, -0.1, 0.4]])
    importance = shap_feature_importance(shap_values, ["a", "b", "c"])
    assert importance.iloc[0]["feature"] == "c"
    assert "mean_abs_shap" in importance.columns


def test_get_expected_value_selects_positive_class() -> None:
    assert get_expected_value(DummyExplainer()) == 0.9
