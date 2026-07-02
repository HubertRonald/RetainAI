from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.cards import info_tip, kpi_card  # noqa: E402
from components.layout import configure_page, render_footer, render_page_shell  # noqa: E402
from modules.dashboard.charts import (  # noqa: E402
    attrition_by_category,
    attrition_distribution,
    attrition_rate_by_category,
    histogram_by_attrition,
)
from modules.io.storage import load_dataframe  # noqa: E402

configure_page()
render_page_shell(
    title="Executive Overview",
    subtitle="High-level attrition analytics and organizational insights",
    icon="overview.svg",
    active_page="executive",
    chips=[("Runtime", "local", "green"), ("View", "historical", "purple")],
)

data_path = PROJECT_ROOT / "data/processed/ibm_hr_attrition_processed.csv"

if not data_path.exists():
    st.warning("Processed dataset not found. Run the data pipeline first.")
    st.stop()

df = load_dataframe(data_path)

st.markdown('<div class="retainai-filter-card">', unsafe_allow_html=True)
filter_cols = st.columns(5)

departments = filter_cols[0].multiselect("Department", sorted(df["Department"].dropna().unique()), default=[])
job_roles = filter_cols[1].multiselect("Job Role", sorted(df["JobRole"].dropna().unique()), default=[])
marital_status = filter_cols[2].multiselect("Marital Status", sorted(df["MaritalStatus"].dropna().unique()), default=[])
overtime = filter_cols[3].multiselect("OverTime", sorted(df["OverTime"].dropna().unique()), default=[])
business_travel = filter_cols[4].multiselect("Business Travel", sorted(df["BusinessTravel"].dropna().unique()), default=[])
st.markdown("</div>", unsafe_allow_html=True)

filtered = df.copy()
if departments:
    filtered = filtered[filtered["Department"].isin(departments)]
if job_roles:
    filtered = filtered[filtered["JobRole"].isin(job_roles)]
if marital_status:
    filtered = filtered[filtered["MaritalStatus"].isin(marital_status)]
if overtime:
    filtered = filtered[filtered["OverTime"].isin(overtime)]
if business_travel:
    filtered = filtered[filtered["BusinessTravel"].isin(business_travel)]

total = len(filtered)
attrition = int((filtered["Attrition"] == "Yes").sum()) if total else 0
active = total - attrition
rate = attrition / total if total else 0
avg_income = filtered["MonthlyIncome"].mean() if total else 0
avg_years = filtered["TotalWorkingYears"].mean() if total else 0

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    kpi_card("Total Employees", f"{total:,}", "Filtered workforce", "👥", "#8b5cf6", svg_icon="data.svg")
with k2:
    kpi_card("Attrition Cases", f"{attrition:,}", "Employees who left", "🧍", "#fb923c", svg_icon="prediction.svg")
with k3:
    kpi_card("Attrition Rate", f"{rate:.2%}", "Current segment risk", "📈", "#ec4899", svg_icon="overview.svg")
with k4:
    kpi_card("Active / Non-Attrition", f"{active:,}", "Retention base", "✅", "#22c55e", svg_icon="survival.svg")
with k5:
    kpi_card("Avg Monthly Income", f"{avg_income/1000:.0f}K", "Across segment", "💳", "#60a5fa", svg_icon="model.svg")
with k6:
    kpi_card("Avg Working Years", f"{avg_years:.1f}", "Experience proxy", "📅", "#a78bfa", svg_icon="api.svg")

row1_left, row1_mid, row1_right = st.columns([1.25, 1.25, 1])
with row1_left:
    st.plotly_chart(attrition_by_category(filtered, "Department", title="Attrition by Department"), use_container_width=True)
with row1_mid:
    st.plotly_chart(attrition_by_category(filtered, "JobRole", title="Attrition by Job Role"), use_container_width=True)
with row1_right:
    st.plotly_chart(attrition_distribution(filtered), use_container_width=True)

row2_left, row2_mid, row2_right = st.columns([1, 1, 1])
with row2_left:
    st.plotly_chart(attrition_by_category(filtered, "OverTime", title="Attrition by OverTime"), use_container_width=True)
with row2_mid:
    st.plotly_chart(attrition_by_category(filtered, "MaritalStatus", title="Attrition by Marital Status"), use_container_width=True)
with row2_right:
    st.plotly_chart(
        attrition_by_category(filtered, "EducationField", title="Attrition by Education Field", orientation="h"),
        use_container_width=True,
    )

with st.expander("Income & Career Progression Analysis", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(histogram_by_attrition(filtered, "MonthlyIncome"), use_container_width=True)
    with c2:
        st.plotly_chart(attrition_rate_by_category(filtered, "YearsAtCompany"), use_container_width=True)

info_tip("Use the filters above to explore workforce segments. All charts update interactively.")
render_footer()
