from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.layout import configure_page, render_footer, render_page_shell  # noqa: E402
from modules.dashboard.survival_loader import get_survival_figures  # noqa: E402

configure_page()

render_page_shell(
    title="Survival Analytics",
    subtitle="Time-aware retention analysis using YearsAtCompany as proxy duration",
    icon="survival.svg",
    active_page="survival",
    chips=[("Method", "Kaplan-Meier", "purple"), ("Duration", "YearsAtCompany", "green")],
)

st.markdown(
    """
    <div class="retainai-card">
        <strong>Interpretation note:</strong>
        the public IBM HR dataset does not provide a true event timestamp.
        RetainAI uses <code>YearsAtCompany</code> as a proxy duration for survival modeling.
    </div>
    """,
    unsafe_allow_html=True,
)

figures = get_survival_figures(PROJECT_ROOT / "artifacts/figures/survival")

tabs = st.tabs(["Overall", "OverTime", "Department", "Job Role", "Hazard Ratios", "Report"])

with tabs[0]:
    path = figures["overall"]
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.info(f"Missing figure: {path}")

with tabs[1]:
    path = figures["overtime"]
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.info(f"Missing figure: {path}")

with tabs[2]:
    path = figures["department"]
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.info(f"Missing figure: {path}")

with tabs[3]:
    path = figures["jobrole"]
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.info(f"Missing figure: {path}")

with tabs[4]:
    path = figures["hazard_ratios"]
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.info(f"Missing figure: {path}")

with tabs[5]:
    report_path = PROJECT_ROOT / "artifacts/reports/survival_report.md"
    if report_path.exists():
        st.markdown(report_path.read_text(encoding="utf-8"))
    else:
        st.info("Survival report not found.")

render_footer()
