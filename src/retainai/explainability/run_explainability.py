from __future__ import annotations

import json

import joblib
import pandas as pd

from modules.classification.preprocessing import build_feature_target
from modules.explainability.explainers import build_shap_explainer
from modules.explainability.feature_importance import shap_feature_importance
from modules.explainability.preprocessing import (
    extract_pipeline_parts,
    sample_background,
    transform_features,
)
from modules.explainability.report import generate_explainability_report
from modules.explainability.shap_values import compute_shap_values, get_expected_value
from modules.explainability.visualization import (
    save_beeswarm_plot,
    save_feature_importance_plot,
    save_waterfall_plot,
)
from modules.io.storage import load_dataframe
from retainai.core.paths import PROJECT_ROOT


def explain_model(model_name: str) -> None:
    model_path = PROJECT_ROOT / "artifacts/models" / f"{model_name}.pkl"
    validation_path = PROJECT_ROOT / "data/validation/ibm_hr_attrition_validation.csv"

    pipeline = joblib.load(model_path)
    validation_df = load_dataframe(validation_path)

    X_val, _ = build_feature_target(
        validation_df,
        target="Attrition",
        positive_class="Yes",
        drop_columns=[
            "EmployeeNumber",
            "EmployeeCount",
            "Over18",
            "StandardHours",
        ],
    )

    _, model = extract_pipeline_parts(pipeline)
    X_transformed, feature_names = transform_features(pipeline, X_val)
    background = sample_background(X_transformed)

    explainer = build_shap_explainer(model, background)
    values = compute_shap_values(explainer, X_transformed)
    expected_value = get_expected_value(explainer)

    importance = shap_feature_importance(values, feature_names)

    explanations_dir = PROJECT_ROOT / "artifacts/explanations" / model_name
    figures_dir = PROJECT_ROOT / "artifacts/figures/explainability" / model_name
    reports_dir = PROJECT_ROOT / "artifacts/reports"

    explanations_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(values, explanations_dir / "shap_values.joblib")
    joblib.dump(expected_value, explanations_dir / "expected_value.joblib")
    importance.to_parquet(explanations_dir / "feature_importance.parquet", index=False)

    (explanations_dir / "metadata.json").write_text(
        json.dumps(
            {
                "model_name": model_name,
                "dataset": "ibm_hr_attrition_validation",
                "n_samples": int(X_transformed.shape[0]),
                "n_features": int(X_transformed.shape[1]),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    save_feature_importance_plot(
        importance,
        figures_dir / "feature_importance.png",
    )
    save_beeswarm_plot(
        values,
        X_transformed,
        feature_names,
        figures_dir / "beeswarm.png",
    )
    save_waterfall_plot(
        values,
        expected_value,
        X_transformed,
        feature_names,
        figures_dir / "waterfall_example.png",
    )

    generate_explainability_report(
        model_name=model_name,
        feature_importance=importance,
        output_path=reports_dir / f"explainability_report_{model_name}.md",
    )

    print(f"Explainability artifacts generated for: {model_name}")


def main() -> None:
    for model_name in ["logistic_regression", "random_forest", "xgboost"]:
        explain_model(model_name)


if __name__ == "__main__":
    main()
