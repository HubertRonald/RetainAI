from __future__ import annotations

import pandas as pd
import streamlit as st

def render_dataframe(df: pd.DataFrame, title: str | None = None) -> None:
    if title:
        st.markdown(f"### {title}")
    st.dataframe(df, use_container_width=True)
