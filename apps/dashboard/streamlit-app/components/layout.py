from __future__ import annotations

import streamlit as st

def configure_page() -> None:
    st.set_page_config(page_title="RetainAI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

def render_header() -> None:
    st.title("RetainAI")
    st.caption("Employee Retention Intelligence Platform")

def render_status_strip(runtime: str, model: str, api_status: str = "offline") -> None:
    cols = st.columns(4)
    cols[0].metric("Runtime", runtime)
    cols[1].metric("Model", model)
    cols[2].metric("Data", "local")
    cols[3].metric("API", api_status)
