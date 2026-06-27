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
from retainai.core.paths import PROJECT_ROOT


def _try_start_mlflow(config: dict):
    try:
        import mlflow

        mlflow_config = config["classification"]["mlflow"]
        if not mlflow_config.get("enabled", False):
            return None

        mlflow.set_tracking_uri(str(PROJECT_ROOT / mlflow_config["tracking_uri"]))
        mlflow.set_experiment(mlflow_config["experiment_name"])
        return mlflow
    except ImportError:
        print("MLflow is not installed. Training will continue without tracking.")
        return None


def main() -> None:
    config_path = PROJECT_ROOT / "configs" / "training.yaml"
    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    cfg = config["classification"]
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

    mlflow = _try_start_mlflow(config)
    results = []

    models_dir = PROJECT_ROOT / "artifacts/models"
    models_dir.mkdir(parents=True, exist_ok=True)

    for model_name in cfg["models"]:
        preprocessor = build_preprocessor(X_train)
        model = build_model(model_name, random_state=random_state)

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model),
            ]
        )

        if mlflow:
            run_context = mlflow.start_run(run_name=model_name)
        else:
            run_context = None

        try:
            if run_context:
                run_context.__enter__()

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

            if mlflow:
                mlflow.log_params(
                    {
                        "model": model_name,
                        "target": target,
                        "positive_class": positive_class,
                    }
                )
                mlflow.log_metrics({k: v for k, v in metrics.items() if k != "model"})
                mlflow.log_artifact(str(model_path))

        finally:
            if run_context:
                run_context.__exit__(None, None, None)

    results_df = metrics_to_dataframe(results)

    results_path = PROJECT_ROOT / "artifacts/reports/classification_metrics.csv"
    results_df.to_csv(results_path, index=False)

    report_path = generate_classification_report(
        results_df,
        output_path=PROJECT_ROOT / "artifacts/reports/classification_report.md",
    )

    metadata_path = PROJECT_ROOT / "artifacts/reports/classification_metadata.json"
    metadata_path.write_text(
        json.dumps({"models": cfg["models"], "target": target}, indent=2),
        encoding="utf-8",
    )

    print(results_df)
    print(f"Classification report generated at: {report_path}")


if __name__ == "__main__":
    main()
