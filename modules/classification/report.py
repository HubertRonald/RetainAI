from __future__ import annotations

from pathlib import Path

import pandas as pd


def generate_classification_report(
    results: pd.DataFrame,
    output_path: str | Path = "artifacts/reports/classification_report.md",
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    content = [
        "# Classification Report",
        "",
        "This report summarizes baseline classification results for employee attrition prediction.",
        "",
        "## Model Comparison",
        "",
        results.to_markdown(index=False),
        "",
        "## Notes",
        "",
        "- Accuracy is not the main metric because the target is imbalanced.",
        "- PR AUC, recall and F1-score are especially relevant for attrition detection.",
        "- Logistic Regression is used as the interpretable baseline.",
        "- Random Forest and XGBoost are used as nonlinear tabular baselines.",
    ]

    path.write_text("\n".join(content), encoding="utf-8")
    return path
