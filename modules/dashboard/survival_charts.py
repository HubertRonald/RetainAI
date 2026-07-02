from __future__ import annotations

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

from modules.dashboard.charts import DARK_LAYOUT, style_fig


def _km_table(
    df: pd.DataFrame,
    duration_col: str = "YearsAtCompany",
    event_col: str = "Attrition",
    positive_class: str = "Yes",
) -> pd.DataFrame:
    data = (
        df[[duration_col, event_col]]
        .dropna()
        .rename(columns={duration_col: "duration", event_col: "event"})
        .copy()
    )
    data["event"] = (data["event"] == positive_class).astype(int)
    data["duration"] = data["duration"].astype(float)

    rows = []
    survival = 1.0

    for t in sorted(data["duration"].unique()):
        at_risk = int((data["duration"] >= t).sum())
        events = int(((data["duration"] == t) & (data["event"] == 1)).sum())

        if at_risk > 0:
            survival *= 1 - (events / at_risk)

        rows.append(
            {
                "duration": t,
                "survival_probability": survival,
                "at_risk": at_risk,
                "events": events,
            }
        )

    return pd.DataFrame(rows)


def interactive_kaplan_meier(
    df: pd.DataFrame,
    duration_col: str = "YearsAtCompany",
    event_col: str = "Attrition",
    title: str = "Kaplan-Meier Survival Curve",
) -> Figure:
    km = _km_table(df, duration_col=duration_col, event_col=event_col)

    fig = px.line(
        km,
        x="duration",
        y="survival_probability",
        markers=True,
        hover_data=["at_risk", "events"],
    )
    fig.update_traces(
        line={"color": "#2f7df6", "width": 3},
        marker={"size": 7, "color": "#8b5cf6"},
        hovertemplate=(
            "<b>Year %{x}</b><br>"
            "Survival: %{y:.2%}<br>"
            "At risk: %{customdata[0]}<br>"
            "Events: %{customdata[1]}<extra></extra>"
        ),
    )
    fig.update_layout(**DARK_LAYOUT)
    fig.update_yaxes(tickformat=".0%")
    return style_fig(fig, title)


def interactive_kaplan_meier_by_group(
    df: pd.DataFrame,
    group_col: str,
    duration_col: str = "YearsAtCompany",
    event_col: str = "Attrition",
    title: str | None = None,
) -> Figure:
    frames = []

    for group, group_df in df.groupby(group_col, dropna=False):
        km = _km_table(group_df, duration_col=duration_col, event_col=event_col)
        km[group_col] = str(group)
        frames.append(km)

    if not frames:
        return style_fig(Figure(), title or f"Kaplan-Meier by {group_col}")

    plot_df = pd.concat(frames, ignore_index=True)

    fig = px.line(
        plot_df,
        x="duration",
        y="survival_probability",
        color=group_col,
        markers=True,
        hover_data=["at_risk", "events"],
    )
    fig.update_traces(
        line={"width": 3},
        marker={"size": 6},
        hovertemplate=(
            "<b>Year %{x}</b><br>"
            "Survival: %{y:.2%}<br>"
            "At risk: %{customdata[0]}<br>"
            "Events: %{customdata[1]}<extra></extra>"
        ),
    )
    fig.update_layout(**DARK_LAYOUT)
    fig.update_yaxes(tickformat=".0%")
    return style_fig(fig, title or f"Kaplan-Meier by {group_col}")
