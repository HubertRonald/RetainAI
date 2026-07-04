from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.cards import info_tip, kpi_grid  # noqa: E402
from components.layout import configure_page, render_footer, render_page_shell  # noqa: E402
from modules.dashboard.charts import (  # noqa: E402
    attrition_by_category,
    attrition_distribution,
    attrition_rate_by_category,
    histogram_by_attrition,
)
from modules.dashboard.export import (  # noqa: E402
    build_dashboard_snapshot_payload,
    dashboard_snapshot_to_json,
    dashboard_snapshot_to_markdown,
    dataframe_to_csv_bytes,
)
from modules.dashboard.visual_export import build_visual_dashboard_zip  # noqa: E402
from modules.io.storage import load_dataframe  # noqa: E402


configure_page()
render_page_shell(
    title="Executive Overview",
    subtitle="High-level attrition analytics and organizational insights",
    icon="overview.svg",
    active_page="executive",
    chips=[
        ("Runtime", "local", "green"),
        ("View", "historical", "purple"),
    ],
)

data_path = PROJECT_ROOT / "data/processed/ibm_hr_attrition_processed.csv"

if not data_path.exists():
    st.warning("Processed dataset not found. Run the data pipeline first.")
    st.stop()

df = load_dataframe(data_path)

filter_cols = st.columns(5, gap="medium")

departments = filter_cols[0].multiselect(
    "Department",
    sorted(df["Department"].dropna().unique()),
    default=[],
    key="overview_department_filter",
)
job_roles = filter_cols[1].multiselect(
    "Job Role",
    sorted(df["JobRole"].dropna().unique()),
    default=[],
    key="overview_jobrole_filter",
)
marital_status = filter_cols[2].multiselect(
    "Marital Status",
    sorted(df["MaritalStatus"].dropna().unique()),
    default=[],
    key="overview_marital_filter",
)
overtime = filter_cols[3].multiselect(
    "OverTime",
    sorted(df["OverTime"].dropna().unique()),
    default=[],
    key="overview_overtime_filter",
)
business_travel = filter_cols[4].multiselect(
    "Business Travel",
    sorted(df["BusinessTravel"].dropna().unique()),
    default=[],
    key="overview_business_travel_filter",
)

st.markdown('<div class="retainai-filter-spacer"></div>', unsafe_allow_html=True)

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

filters = {
    "Department": departments,
    "JobRole": job_roles,
    "MaritalStatus": marital_status,
    "OverTime": overtime,
    "BusinessTravel": business_travel,
}

kpis = {
    "total_employees": total,
    "attrition_cases": attrition,
    "attrition_rate": f"{rate:.2%}",
    "active_non_attrition": active,
    "avg_monthly_income": round(float(avg_income), 2) if total else 0,
    "avg_total_working_years": round(float(avg_years), 2) if total else 0,
}

snapshot = build_dashboard_snapshot_payload(
    filters=filters,
    kpis=kpis,
    row_count=total,
    source="local",
)

kpi_grid(
    [
        {"label": "Total Employees", "value": f"{total:,}", "helper": "Filtered workforce", "icon": "👥", "accent": "#8b5cf6", "svg_icon": "data.svg"},
        {"label": "Attrition Cases", "value": f"{attrition:,}", "helper": "Employees who left", "icon": "🧍", "accent": "#fb923c", "svg_icon": "prediction.svg"},
        {"label": "Attrition Rate", "value": f"{rate:.2%}", "helper": "Current segment risk", "icon": "📈", "accent": "#ec4899", "svg_icon": "overview.svg"},
        {"label": "Active / Non-Attrition", "value": f"{active:,}", "helper": "Retention base", "icon": "✅", "accent": "#22c55e", "svg_icon": "survival.svg"},
        {"label": "Avg Monthly Income", "value": f"{avg_income/1000:.0f}K", "helper": "Across segment", "icon": "💳", "accent": "#60a5fa", "svg_icon": "model.svg"},
        {"label": "Avg Working Years", "value": f"{avg_years:.1f}", "helper": "Experience proxy", "icon": "📅", "accent": "#a78bfa", "svg_icon": "api.svg"},
    ]
)

fig_department = attrition_by_category(filtered, "Department", title="Attrition by Department")
fig_jobrole = attrition_by_category(filtered, "JobRole", title="Attrition by Job Role")
fig_distribution = attrition_distribution(filtered)
fig_overtime = attrition_by_category(filtered, "OverTime", title="Attrition by OverTime")
fig_marital = attrition_by_category(filtered, "MaritalStatus", title="Attrition by Marital Status")
fig_education = attrition_by_category(
    filtered,
    "EducationField",
    title="Attrition by Education Field",
    orientation="h",
)

visual_figures = {
    "attrition_by_department": fig_department,
    "attrition_by_job_role": fig_jobrole,
    "attrition_distribution": fig_distribution,
    "attrition_by_overtime": fig_overtime,
    "attrition_by_marital_status": fig_marital,
    "attrition_by_education_field": fig_education,
}

export_cols = st.columns([1.15, 1.15, 1.15, 1.35], gap="small")
with export_cols[0]:
    st.download_button(
        "Export snapshot MD",
        data=dashboard_snapshot_to_markdown(snapshot).encode("utf-8"),
        file_name="retainai_dashboard_snapshot.md",
        mime="text/markdown",
    )
with export_cols[1]:
    st.download_button(
        "Export filtered CSV",
        data=dataframe_to_csv_bytes(filtered),
        file_name="retainai_filtered_dashboard_data.csv",
        mime="text/csv",
    )
with export_cols[2]:
    st.download_button(
        "Export snapshot JSON",
        data=dashboard_snapshot_to_json(snapshot).encode("utf-8"),
        file_name="retainai_dashboard_snapshot.json",
        mime="application/json",
    )

with export_cols[3]:
    try:
        visual_zip = build_visual_dashboard_zip(
            figures=visual_figures,
            snapshot_payload=snapshot,
            filtered_df=filtered,
            image_format="png",
        )
        st.download_button(
            "Export visual ZIP",
            data=visual_zip,
            file_name="retainai_dashboard_visual_export.zip",
            mime="application/zip",
        )
    except RuntimeError as exc:
        st.caption(str(exc))

st.markdown('<div class="retainai-section-break"></div>', unsafe_allow_html=True)


row1_left, row1_mid, row1_right = st.columns([1.25, 1.25, 1], gap="medium")
with row1_left:
    st.plotly_chart(fig_department, use_container_width=True)
with row1_mid:
    st.plotly_chart(fig_jobrole, use_container_width=True)
with row1_right:
    st.plotly_chart(fig_distribution, use_container_width=True)

row2_left, row2_mid, row2_right = st.columns([1, 1, 1], gap="medium")
with row2_left:
    st.plotly_chart(fig_overtime, use_container_width=True)
with row2_mid:
    st.plotly_chart(fig_marital, use_container_width=True)
with row2_right:
    st.plotly_chart(fig_education, use_container_width=True)

with st.expander("Income & Career Progression Analysis", expanded=False):
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.plotly_chart(histogram_by_attrition(filtered, "MonthlyIncome"), use_container_width=True)
    with c2:
        st.plotly_chart(attrition_rate_by_category(filtered, "YearsAtCompany"), use_container_width=True)

info_tip("Use filters to explore workforce segments. Charts and exports update with the selected segment.")

render_footer()
