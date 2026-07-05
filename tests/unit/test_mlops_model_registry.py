from __future__ import annotations

from modules.mlops.model_registry import (
    build_model_version_record,
    load_model_registry_manifest,
    update_model_registry_manifest,
)
from modules.mlops.tracking import registered_model_name


def test_registered_model_name_respects_config() -> None:
    config = {
        "registry_enabled": True,
        "registered_model_prefix": "retainai",
    }
    assert registered_model_name("xgboost", config) == "retainai_xgboost"


def test_registered_model_name_can_be_disabled() -> None:
    config = {"registry_enabled": False}
    assert registered_model_name("xgboost", config) is None


def test_model_registry_manifest_can_be_updated(tmp_path) -> None:
    path = tmp_path / "model_registry.json"
    record = build_model_version_record(
        model_name="logistic_regression",
        model_path="artifacts/models/logistic_regression.pkl",
        metrics={"roc_auc": 0.8},
        run_id="abc123",
        experiment_name="retainai-classification",
        registered_model_name="retainai_logistic_regression",
    )

    update_model_registry_manifest(record, registry_path=path)
    registry = load_model_registry_manifest(path)

    assert "logistic_regression" in registry["models"]
    assert registry["latest"]["logistic_regression"]["run_id"] == "abc123"
