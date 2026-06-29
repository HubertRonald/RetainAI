from __future__ import annotations

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


COLOR_NO = "#2f7df6"
COLOR_YES = "#ec4899"
COLOR_MAP = {"No": COLOR_NO, "Yes": COLOR_YES}

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
    )
    fig.update_yaxes(
        gridcolor="rgba(148,163,184,0.14)",
        zerolinecolor="rgba(148,163,184,0.24)",
        linecolor="rgba(148,163,184,0.28)",
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
    )
    return style_fig(fig, "Attrition Distribution")


def attrition_by_category(
        df: pd.DataFrame,
        category: str,
        target: str = "Attrition",
        title: str | None = None,
        orientation: str = "v",
    ) -> Figure:
    grouped = (
        df.groupby([category, target], dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

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

    fig.update_traces(textposition="outside")
    return style_fig(fig, title or f"Attrition by {category}")


def attrition_rate_by_category(
        df: pd.DataFrame,
        category: str,
        target: str = "Attrition",
    ) -> Figure:
    grouped = (
        df.groupby(category, dropna=False)[target]
        .apply(lambda s: (s == "Yes").mean() * 100)
        .reset_index(name="attrition_rate")
        .sort_values("attrition_rate", ascending=False)
    )

    fig = px.bar(
        grouped,
        x=category,
        y="attrition_rate",
        text=grouped["attrition_rate"].round(1),
        color="attrition_rate",
        color_continuous_scale=["#2f7df6", "#ec4899"],
    )
    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Attrition Rate: %{y:.1f}%<extra></extra>",
    )
    return style_fig(fig, f"Attrition Rate by {category}")


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
    return style_fig(fig, f"{column} Distribution by Attrition")
