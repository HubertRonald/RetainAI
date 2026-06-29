from __future__ import annotations

import streamlit as st

def kpi_card(label: str, value, help_text: str | None = None) -> None:
    st.metric(label=label, value=value, help=help_text)
