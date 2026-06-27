from __future__ import annotations

from modules.classification.metrics import evaluate_classifier, metrics_to_dataframe
from modules.classification.models import build_model
from modules.classification.preprocessing import (
    build_feature_target,
    build_preprocessor,
)


def test_build_feature_target(sample_hr_df) -> None:
    X, y = build_feature_target(
        sample_hr_df,
        target="Attrition",
        positive_class="Yes",
        drop_columns=["EmployeeNumber", "EmployeeCount", "Over18", "StandardHours"],
    )
    assert "Attrition" not in X.columns
    assert set(y.unique()) == {0, 1}


def test_build_preprocessor_can_transform(sample_hr_df) -> None:
    X, _ = build_feature_target(sample_hr_df, drop_columns=["EmployeeNumber"])
    transformed = build_preprocessor(X).fit_transform(X)
    assert transformed.shape[0] == len(sample_hr_df)


def test_build_logistic_regression_model() -> None:
    assert build_model("logistic_regression").__class__.__name__ == "LogisticRegression"


def test_evaluate_classifier_returns_expected_metrics() -> None:
    metrics = evaluate_classifier(
        y_true=[0, 1, 0, 1],
        y_pred=[0, 1, 0, 0],
        y_proba=[0.1, 0.8, 0.2, 0.4],
        model_name="test_model",
    )
    assert metrics["model"] == "test_model"
    assert "roc_auc" in metrics
    assert "pr_auc" in metrics


def test_metrics_to_dataframe_sorts_by_pr_auc() -> None:
    df = metrics_to_dataframe(
        [{"model": "a", "pr_auc": 0.1}, {"model": "b", "pr_auc": 0.9}]
    )
    assert df.iloc[0]["model"] == "b"
