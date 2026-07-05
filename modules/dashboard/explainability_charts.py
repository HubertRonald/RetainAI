from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

from modules.dashboard.charts import style_fig


def load_feature_importance(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        return pd.DataFrame()

    if path.suffix == ".parquet":
        return pd.read_parquet(path)

    if path.suffix == ".csv":
        return pd.read_csv(path)

    return pd.DataFrame()


def interactive_feature_importance(
    importance_df: pd.DataFrame,
    top_n: int = 20,
) -> Figure:
    if importance_df.empty:
        return style_fig(Figure(), "Global Feature Importance")

    df = importance_df.copy()

    feature_col = "feature" if "feature" in df.columns else df.columns[0]
    value_col = (
        "mean_abs_shap"
        if "mean_abs_shap" in df.columns
        else "importance" if "importance" in df.columns else df.columns[-1]
    )

    df = df.sort_values(value_col, ascending=False).head(top_n)

    fig = px.bar(
        df.sort_values(value_col, ascending=True),
        x=value_col,
        y=feature_col,
        orientation="h",
        color=value_col,
        color_continuous_scale=["#2f7df6", "#8b5cf6", "#ec4899"],
        text=value_col,
    )

    fig.update_traces(
        texttemplate="%{text:.3f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>",
    )
    fig.update_layout(coloraxis_showscale=False)
    return style_fig(fig, "Interactive Global SHAP Feature Importance")


def load_shap_values(path: str | Path):
    path = Path(path)
    if not path.exists():
        return None
    return joblib.load(path)


def _select_positive_class(values):
    if isinstance(values, list):
        return values[1] if len(values) > 1 else values[0]

    if isinstance(values, tuple):
        return values[1] if len(values) > 1 else values[0]

    arr = np.asarray(values)

    if arr.ndim == 3:
        return arr[:, :, 1] if arr.shape[-1] > 1 else arr[:, :, 0]

    return arr


def interactive_shap_distribution(
    shap_values,
    feature_names: list[str],
    top_n: int = 20,
) -> Figure:
    if shap_values is None or not feature_names:
        return style_fig(Figure(), "Interactive SHAP Distribution")

    values = _select_positive_class(shap_values)
    values = np.asarray(values)

    if values.ndim != 2:
        return style_fig(Figure(), "Interactive SHAP Distribution")

    mean_abs = np.abs(values).mean(axis=0)
    top_idx = np.argsort(mean_abs)[::-1][:top_n]
    top_features = [feature_names[idx] for idx in top_idx]

    rows = []
    for rank, idx in enumerate(top_idx):
        for value in values[:, idx]:
            rows.append(
                {
                    "feature": top_features[rank],
                    "shap_value": float(value),
                    "direction": "Increases risk" if value >= 0 else "Reduces risk",
                }
            )

    plot_df = pd.DataFrame(rows)

    fig = px.strip(
        plot_df,
        x="shap_value",
        y="feature",
        color="direction",
        color_discrete_map={
            "Increases risk": "#ec4899",
            "Reduces risk": "#2f7df6",
        },
        stripmode="overlay",
    )

    fig.update_traces(
        jitter=0.35,
        marker={"opacity": 0.65, "size": 6},
        hovertemplate="<b>%{y}</b><br>SHAP value: %{x:.4f}<extra></extra>",
    )

    fig.update_layout(
        yaxis={"categoryorder": "array", "categoryarray": top_features[::-1]}
    )
    return style_fig(fig, "Interactive SHAP Value Distribution")
