from __future__ import annotations

import pandas as pd
import streamlit as st


def render_dataframe(
    df: pd.DataFrame,
    title: str | None = None,
    max_rows: int | None = None,
) -> None:
    if title:
        st.markdown(f"### {title}")

    view = df.head(max_rows) if max_rows else df
    st.dataframe(view, use_container_width=True)


def render_compact_table(
    df: pd.DataFrame,
    title: str | None = None,
    max_rows: int = 15,
) -> None:
    render_dataframe(df, title=title, max_rows=max_rows)


def render_missing_table_message(message: str) -> None:
    st.info(message)
