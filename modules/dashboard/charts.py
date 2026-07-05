from __future__ import annotations

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

COLOR_NO = "#2f7df6"
COLOR_YES = "#ec4899"
COLOR_MAP = {"No": COLOR_NO, "Yes": COLOR_YES}

COLOR_PURPLE = "#8b5cf6"
COLOR_GREEN = "#22c55e"
COLOR_ORANGE = "#fb923c"
COLOR_RED = "#ef4444"
COLOR_MUTED = "#94a3b8"

DARK_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font_color": "#e2e8f0",
    "legend_title_font_color": "#cbd5e1",
    "legend_font_color": "#cbd5e1",
    "margin": dict(l=30, r=25, t=55, b=45),
}


def style_fig(fig: Figure, title: str | None = None) -> Figure:
    fig.update_layout(
        template="plotly_dark",
        title=title,
        **DARK_LAYOUT,
    )
    fig.update_xaxes(
        gridcolor="rgba(148,163,184,0.14)",
        zerolinecolor="rgba(148,163,184,0.24)",
        linecolor="rgba(148,163,184,0.28)",
        tickfont={"color": "#cbd5e1"},
        title_font={"color": "#cbd5e1"},
    )
    fig.update_yaxes(
        gridcolor="rgba(148,163,184,0.14)",
        zerolinecolor="rgba(148,163,184,0.24)",
        linecolor="rgba(148,163,184,0.28)",
        tickfont={"color": "#cbd5e1"},
        title_font={"color": "#cbd5e1"},
    )
    return fig


def attrition_distribution(df: pd.DataFrame, target: str = "Attrition") -> Figure:
    counts = df[target].value_counts().reset_index()
    counts.columns = [target, "count"]

    fig = px.pie(
        counts,
        names=target,
        values="count",
        hole=0.58,
        color=target,
        color_discrete_map=COLOR_MAP,
    )
    fig.update_traces(
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Employees: %{value}<br>Share: %{percent}<extra></extra>",
        marker={"line": {"color": "rgba(15,23,42,0.8)", "width": 2}},
    )
    return style_fig(fig, "Attrition Distribution")


def attrition_by_category(
    df: pd.DataFrame,
    category: str,
    target: str = "Attrition",
    title: str | None = None,
    orientation: str = "v",
    top_n: int | None = None,
) -> Figure:
    grouped = (
        df.groupby([category, target], dropna=False).size().reset_index(name="count")
    )

    if top_n is not None:
        order = (
            grouped.groupby(category, dropna=False)["count"]
            .sum()
            .sort_values(ascending=False)
            .head(top_n)
            .index
        )
        grouped = grouped[grouped[category].isin(order)]

    if orientation == "h":
        fig = px.bar(
            grouped,
            y=category,
            x="count",
            color=target,
            barmode="group",
            color_discrete_map=COLOR_MAP,
            text="count",
            orientation="h",
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
    else:
        fig = px.bar(
            grouped,
            x=category,
            y="count",
            color=target,
            barmode="group",
            color_discrete_map=COLOR_MAP,
            text="count",
        )

    fig.update_traces(
        textposition="outside",
        marker_line_color="rgba(255,255,255,0.12)",
        marker_line_width=1,
        hovertemplate=(
            "<b>%{x}</b><br>Employees: %{y}<extra></extra>"
            if orientation == "v"
            else "<b>%{y}</b><br>Employees: %{x}<extra></extra>"
        ),
    )

    return style_fig(fig, title or f"Attrition by {category}")


def attrition_rate_by_category(
    df: pd.DataFrame,
    category: str,
    target: str = "Attrition",
    title: str | None = None,
    top_n: int | None = None,
) -> Figure:
    grouped = (
        df.groupby(category, dropna=False)[target]
        .apply(lambda s: (s == "Yes").mean() * 100)
        .reset_index(name="attrition_rate")
        .sort_values("attrition_rate", ascending=False)
    )

    if top_n is not None:
        grouped = grouped.head(top_n)

    fig = px.bar(
        grouped,
        x=category,
        y="attrition_rate",
        text=grouped["attrition_rate"].round(1),
        color="attrition_rate",
        color_continuous_scale=["#2f7df6", "#8b5cf6", "#ec4899"],
    )
    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Attrition Rate: %{y:.1f}%<extra></extra>",
    )
    fig.update_layout(coloraxis_showscale=False)

    return style_fig(fig, title or f"Attrition Rate by {category}")


def histogram_by_attrition(
    df: pd.DataFrame,
    column: str,
    target: str = "Attrition",
    nbins: int = 20,
) -> Figure:
    fig = px.histogram(
        df,
        x=column,
        color=target,
        nbins=nbins,
        barmode="group",
        color_discrete_map=COLOR_MAP,
    )
    fig.update_traces(
        hovertemplate=f"<b>{column}</b>: %{{x}}<br>Employees: %{{y}}<extra></extra>"
    )
    return style_fig(fig, f"{column} Distribution by Attrition")


def stacked_attrition_by_category(
    df: pd.DataFrame,
    category: str,
    target: str = "Attrition",
    title: str | None = None,
) -> Figure:
    grouped = (
        df.groupby([category, target], dropna=False).size().reset_index(name="count")
    )
    fig = px.bar(
        grouped,
        y=category,
        x="count",
        color=target,
        orientation="h",
        color_discrete_map=COLOR_MAP,
        text="count",
    )
    fig.update_traces(textposition="inside")
    fig.update_layout(barmode="stack", yaxis={"categoryorder": "total ascending"})
    return style_fig(fig, title or f"Attrition by {category}")
