from __future__ import annotations

import html

import streamlit as st


def kpi_card(
        label: str,
        value: str | int | float,
        helper: str = "",
        icon: str = "●",
        accent: str = "#615fff",
    ) -> None:
    st.markdown(
        f"""
        <div class="retainai-card retainai-kpi-card">
            <div class="retainai-kpi-icon" style="color:{accent};">
                <span style="font-size:1.45rem;">{html.escape(icon)}</span>
            </div>
            <div>
                <div class="retainai-kpi-label">{html.escape(label)}</div>
                <div class="retainai-kpi-value">{html.escape(str(value))}</div>
                <div class="retainai-kpi-help" style="color:{accent};">{html.escape(helper)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_tip(message: str) -> None:
    st.markdown(
        f"""
        <div class="retainai-card" style="margin-top:1rem;">
            <span class="retainai-chip purple">Tip</span>
            <span style="margin-left:.5rem;color:#cbd5e1;">{html.escape(message)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
