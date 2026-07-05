from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.layout import configure_page, render_footer, render_page_shell  # noqa: E402
from modules.dashboard.survival_charts import (  # noqa: E402
    interactive_kaplan_meier,
    interactive_kaplan_meier_by_group,
)
from modules.io.storage import load_dataframe  # noqa: E402

configure_page()

render_page_shell(
    title="Survival Analytics",
    subtitle="Time-aware retention analysis using YearsAtCompany as proxy duration",
    icon="survival.svg",
    active_page="survival",
    chips=[
        ("Method", "Kaplan-Meier", "purple"),
        ("Duration", "YearsAtCompany", "green"),
    ],
)

data_path = PROJECT_ROOT / "data/processed/ibm_hr_attrition_processed.csv"

if not data_path.exists():
    st.warning("Processed dataset not found. Run the data pipeline first.")
    render_footer()
    st.stop()

df = load_dataframe(data_path)

st.markdown(
    """
    <div class="retainai-card">
        <strong>Interpretation note:</strong>
        the public IBM HR dataset does not provide a true event timestamp.
        RetainAI uses <code>YearsAtCompany</code> as a proxy duration for survival-style visualization.
    </div>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs(["Overall", "OverTime", "Department", "Job Role", "Report"])

with tabs[0]:
    st.plotly_chart(
        interactive_kaplan_meier(df),
        use_container_width=True,
    )

with tabs[1]:
    st.plotly_chart(
        interactive_kaplan_meier_by_group(df, "OverTime"),
        use_container_width=True,
    )

with tabs[2]:
    st.plotly_chart(
        interactive_kaplan_meier_by_group(df, "Department"),
        use_container_width=True,
    )

with tabs[3]:
    st.plotly_chart(
        interactive_kaplan_meier_by_group(df, "JobRole"),
        use_container_width=True,
    )

with tabs[4]:
    report_path = PROJECT_ROOT / "artifacts/reports/survival_report.md"
    if report_path.exists():
        st.markdown(report_path.read_text(encoding="utf-8"))
    else:
        st.info("Survival report not found.")

render_footer()
