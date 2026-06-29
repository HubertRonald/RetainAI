from __future__ import annotations

import sys
from pathlib import Path
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[4]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.dashboard.charts import attrition_by_category, attrition_distribution  # noqa: E402
from modules.io.storage import load_dataframe  # noqa: E402

st.title("Executive Overview")
data_path = PROJECT_ROOT / "data/processed/ibm_hr_attrition_processed.csv"

if not data_path.exists():
    st.warning("Processed dataset not found. Run the data pipeline first.")
    st.stop()
df = load_dataframe(data_path)
total = len(df)
attrition = int((df["Attrition"] == "Yes").sum())
rate = attrition / total if total else 0
cols = st.columns(4)
cols[0].metric("Total Employees", total)
cols[1].metric("Attrition Cases", attrition)
cols[2].metric("Attrition Rate", f"{rate:.2%}")
cols[3].metric("Active / Non-Attrition", total - attrition)
left, right = st.columns([2, 1])
with left:
    st.plotly_chart(attrition_by_category(df, "Department"), use_container_width=True)
with right:
    st.plotly_chart(attrition_distribution(df), use_container_width=True)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(attrition_by_category(df, "JobRole"), use_container_width=True)
with col2:
    st.plotly_chart(attrition_by_category(df, "OverTime"), use_container_width=True)
col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(attrition_by_category(df, "BusinessTravel"), use_container_width=True)
with col4:
    st.plotly_chart(attrition_by_category(df, "MaritalStatus"), use_container_width=True)
st.markdown("### Data Preview")
st.dataframe(df.head(20), use_container_width=True)
