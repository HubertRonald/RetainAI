from __future__ import annotations

import json

import joblib
import yaml
from sklearn.pipeline import Pipeline

from modules.classification.metrics import evaluate_classifier, metrics_to_dataframe
from modules.classification.models import build_model
from modules.classification.preprocessing import (
    build_feature_target,
    build_preprocessor,
)
from modules.classification.report import generate_classification_report
from modules.io.storage import load_dataframe
from modules.mlops.model_registry import (
    build_model_version_record,
    update_model_registry_manifest,
)
from modules.mlops.tracking import (
    log_classification_run,
    registered_model_name,
    setup_mlflow_tracking,
)
from retainai.core.paths import PROJECT_ROOT


def main() -> None:
    config_path = PROJECT_ROOT / "configs" / "training.yaml"

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    cfg = config["classification"]
    mlflow_config = cfg.get("mlflow", {})

    target = cfg["target"]
    positive_class = cfg["positive_class"]
    random_state = cfg["random_state"]

    train_df = load_dataframe(PROJECT_ROOT / "data/train/ibm_hr_attrition_train.csv")
    validation_df = load_dataframe(
        PROJECT_ROOT / "data/validation/ibm_hr_attrition_validation.csv"
    )

    X_train, y_train = build_feature_target(
        train_df,
        target=target,
        positive_class=positive_class,
        drop_columns=cfg["drop_columns"],
    )
    X_val, y_val = build_feature_target(
        validation_df,
        target=target,
        positive_class=positive_class,
        drop_columns=cfg["drop_columns"],
    )

    mlflow, infer_signature = setup_mlflow_tracking(
        mlflow_config=mlflow_config,
        project_root=PROJECT_ROOT,
    )

    results = []
    models_dir = PROJECT_ROOT / "artifacts/models"
    reports_dir = PROJECT_ROOT / "artifacts/reports"

    models_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    for model_name in cfg["models"]:
        preprocessor = build_preprocessor(X_train)
        try:
            model = build_model(model_name, random_state=random_state)
        except ImportError as exc:
            print(
                f"Skipping model '{model_name}' because dependency is unavailable: {exc}"
            )
            continue

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model),
            ]
        )

        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_val)
        y_proba = pipeline.predict_proba(X_val)[:, 1]

        metrics = evaluate_classifier(
            y_true=y_val,
            y_pred=y_pred,
            y_proba=y_proba,
            model_name=model_name,
        )
        results.append(metrics)

        model_path = models_dir / f"{model_name}.pkl"
        joblib.dump(pipeline, model_path)

        params = {
            "model": model_name,
            "target": target,
            "positive_class": positive_class,
            "random_state": random_state,
            "train_rows": len(X_train),
            "validation_rows": len(X_val),
        }

        run_id = log_classification_run(
            mlflow=mlflow,
            infer_signature=infer_signature,
            pipeline=pipeline,
            model_name=model_name,
            metrics=metrics,
            params=params,
            X_train=X_train,
            X_val=X_val,
            model_path=model_path,
            report_paths=[],
            mlflow_config=mlflow_config,
        )

        record = build_model_version_record(
            model_name=model_name,
            model_path=model_path.relative_to(PROJECT_ROOT),
            metrics=metrics,
            run_id=run_id,
            experiment_name=mlflow_config.get("experiment_name"),
            registered_model_name=registered_model_name(model_name, mlflow_config),
        )
        update_model_registry_manifest(
            record=record,
            registry_path=PROJECT_ROOT / "artifacts/models/model_registry.json",
        )

    results_df = metrics_to_dataframe(results)

    results_path = reports_dir / "classification_metrics.csv"
    results_df.to_csv(results_path, index=False)

    report_path = generate_classification_report(
        results_df,
        output_path=reports_dir / "classification_report.md",
    )

    metadata_path = reports_dir / "classification_metadata.json"
    metadata_path.write_text(
        json.dumps(
            {
                "models": cfg["models"],
                "target": target,
                "mlflow": {
                    "enabled": bool(mlflow),
                    "tracking_uri": mlflow_config.get("tracking_uri"),
                    "experiment_name": mlflow_config.get("experiment_name"),
                    "registry_enabled": mlflow_config.get("registry_enabled", False),
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(results_df)
    print(f"Classification report generated at: {report_path}")
    print(f"Model registry manifest updated at: {models_dir / 'model_registry.json'}")

    if mlflow:
        print(
            "MLflow tracking complete. Run: "
            "mlflow ui --backend-store-uri artifacts/mlflow --port 5000"
        )


if __name__ == "__main__":
    main()
