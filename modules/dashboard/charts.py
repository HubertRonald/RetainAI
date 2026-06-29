from __future__ import annotations

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


def style_fig(fig: Figure) -> Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1d293d",
        plot_bgcolor="#1d293d",
        font_color="#e2e8f0",
        legend_bgcolor="#1d293d",
        legend_bordercolor="#314158",
        margin=dict(l=20, r=20, t=50, b=30),
    )
    return fig


def attrition_distribution(df: pd.DataFrame, target: str = "Attrition") -> Figure:
    counts = df[target].value_counts().reset_index()
    counts.columns = [target, "count"]
    return style_fig(px.pie(counts, names=target, values="count", hole=0.45))


def attrition_by_category(
    df: pd.DataFrame, category: str, target: str = "Attrition"
) -> Figure:
    grouped = (
        df.groupby([category, target], dropna=False).size().reset_index(name="count")
    )
    return style_fig(
        px.bar(grouped, x=category, y="count", color=target, barmode="group")
    )
