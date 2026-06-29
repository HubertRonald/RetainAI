from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.layout import configure_page, render_footer, render_page_shell  # noqa: E402

configure_page()

runtime = os.getenv("RETAINAI_DASHBOARD_MODE", "local")
model = st.session_state.get("selected_model", "logistic_regression")

render_page_shell(
    title="RetainAI",
    subtitle="Employee Retention Intelligence Platform",
    icon="retainai.svg",
    active_page="home",
    chips=[
        ("Runtime", runtime, "green"),
        ("Model", model, "purple"),
        ("API", "offline", "red"),
    ],
)

st.markdown(
    """
    <div class="retainai-card">
        <h2 style="margin-top:0;">Dashboard Foundation</h2>
        <p style="color:#cbd5e1;">
            Navigate through the sidebar to explore historical attrition analytics,
            prediction workflows, model explainability and survival analysis.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_footer()
