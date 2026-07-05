from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def import_mlflow():
    try:
        import mlflow
        import mlflow.sklearn
        from mlflow.models import infer_signature

        return mlflow, infer_signature
    except ImportError:
        return None, None


def resolve_tracking_uri(
    raw_tracking_uri: str,
    project_root: Path,
) -> str:
    """Resolve local MLflow tracking paths as absolute file:// URIs.

    This avoids cross-environment path leaks such as `/workspace` from
    DevContainers/Docker being reused when training is executed on macOS.
    """

    if raw_tracking_uri.startswith(
        ("http://", "https://", "databricks", "sqlite:", "file:")
    ):
        return raw_tracking_uri

    tracking_path = Path(raw_tracking_uri)
    if not tracking_path.is_absolute():
        tracking_path = project_root / tracking_path

    tracking_path = tracking_path.resolve()
    tracking_path.mkdir(parents=True, exist_ok=True)

    return tracking_path.as_uri()


def setup_mlflow_tracking(
    mlflow_config: dict[str, Any],
    project_root: Path,
):
    mlflow, infer_signature = import_mlflow()

    if mlflow is None:
        print("MLflow is not installed. Training will continue without tracking.")
        return None, None

    if not mlflow_config.get("enabled", False):
        return None, None

    tracking_uri = resolve_tracking_uri(
        raw_tracking_uri=mlflow_config.get("tracking_uri", "artifacts/mlflow"),
        project_root=project_root,
    )

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(
        mlflow_config.get("experiment_name", "retainai-classification")
    )

    print(f"MLflow tracking URI: {tracking_uri}")

    return mlflow, infer_signature


def registered_model_name(
    model_name: str,
    mlflow_config: dict[str, Any],
) -> str | None:
    if not mlflow_config.get("registry_enabled", False):
        return None

    prefix = mlflow_config.get("registered_model_prefix", "retainai")
    return f"{prefix}_{model_name}"


def log_classification_run(
    mlflow,
    infer_signature,
    pipeline,
    model_name: str,
    metrics: dict[str, Any],
    params: dict[str, Any],
    X_train: pd.DataFrame,
    X_val: pd.DataFrame,
    model_path: Path,
    report_paths: list[Path],
    mlflow_config: dict[str, Any],
) -> str | None:
    if mlflow is None:
        return None

    run_id: str | None = None
    model_registry_name = registered_model_name(model_name, mlflow_config)

    with mlflow.start_run(run_name=model_name) as run:
        run_id = run.info.run_id

        mlflow.log_params(params)
        mlflow.log_metrics({k: float(v) for k, v in metrics.items() if k != "model"})

        for report_path in report_paths:
            if report_path.exists():
                mlflow.log_artifact(str(report_path), artifact_path="reports")

        if model_path.exists():
            mlflow.log_artifact(str(model_path), artifact_path="pickle")

        signature = None
        input_example = None

        if mlflow_config.get("log_model_signature", True):
            try:
                sample = X_val.head(5)
                predictions = pipeline.predict_proba(sample)[:, 1]
                signature = infer_signature(sample, predictions)
            except Exception as exc:  # noqa: BLE001
                print(f"Could not infer MLflow model signature: {exc}")

        if mlflow_config.get("log_input_example", True):
            input_example = X_train.head(5)

        try:
            mlflow.sklearn.log_model(
                sk_model=pipeline,
                artifact_path="model",
                registered_model_name=model_registry_name,
                signature=signature,
                input_example=input_example,
            )
        except Exception as exc:  # noqa: BLE001
            print(
                "Could not register/log model with registered_model_name. "
                f"Retrying without registry name. Details: {exc}"
            )
            mlflow.sklearn.log_model(
                sk_model=pipeline,
                artifact_path="model",
                signature=signature,
                input_example=input_example,
            )

        mlflow.set_tags(
            {
                "project": "RetainAI",
                "task": "employee_attrition_prediction",
                "model_name": model_name,
                "framework": "scikit-learn",
            }
        )

    return run_id
