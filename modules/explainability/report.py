from __future__ import annotations

from pathlib import Path

import pandas as pd


def generate_explainability_report(
    model_name: str,
    feature_importance: pd.DataFrame,
    output_path: str | Path,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    content = [
        "# Explainability Report",
        "",
        f"Model explained: `{model_name}`",
        "",
        "## Global SHAP Feature Importance",
        "",
        feature_importance.head(25).to_markdown(index=False),
        "",
        "## Notes",
        "",
        "- SHAP values explain feature contributions to model predictions.",
        "- Global importance is computed as mean absolute SHAP value.",
        "- Local explanations are generated for representative validation samples.",
    ]

    path.write_text("\n".join(content), encoding="utf-8")
    return path
