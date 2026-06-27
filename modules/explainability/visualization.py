from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import shap


def save_feature_importance_plot(
        importance_df: pd.DataFrame,
        output_path: str | Path,
        top_n: int = 20,
    ) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    plot_df = importance_df.head(top_n).sort_values("mean_abs_shap")

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(plot_df["feature"], plot_df["mean_abs_shap"])
    ax.set_title("Global SHAP Feature Importance")
    ax.set_xlabel("Mean |SHAP value|")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()

    return path


def save_beeswarm_plot(shap_values, X, feature_names, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    shap.summary_plot(shap_values, X, feature_names=feature_names, show=False)
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()

    return path


def save_waterfall_plot(
        shap_values,
        expected_value,
        X,
        feature_names,
        output_path: str | Path,
        sample_index: int = 0,
    ) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    explanation = shap.Explanation(
        values=shap_values[sample_index],
        base_values=expected_value,
        data=X[sample_index],
        feature_names=feature_names,
    )

    shap.plots.waterfall(explanation, show=False, max_display=15)
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()

    return path
