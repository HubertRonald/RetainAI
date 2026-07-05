from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.layout import configure_page, render_footer, render_page_shell  # noqa: E402
from components.tables import render_dataframe  # noqa: E402
from modules.io.storage import load_dataframe  # noqa: E402

configure_page()

render_page_shell(
    title="Data Dictionary",
    subtitle="Column-level reference for RetainAI dashboard and prediction workflows",
    icon="data.svg",
    active_page="data_dictionary",
    chips=[
        ("Source", "processed dataset", "green"),
        ("Scope", "dashboard", "purple"),
    ],
)

data_path = PROJECT_ROOT / "data/processed/ibm_hr_attrition_processed.csv"

if not data_path.exists():
    st.warning("Processed dataset not found. Run the data pipeline first.")
    render_footer()
    st.stop()

df = load_dataframe(data_path)

dictionary = pd.DataFrame(
    {
        "column": df.columns,
        "dtype": [str(dtype) for dtype in df.dtypes],
        "missing_values": [int(df[col].isna().sum()) for col in df.columns],
        "unique_values": [int(df[col].nunique(dropna=True)) for col in df.columns],
        "dashboard_usage": [
            "target" if col == "Attrition"
            else "filter/chart" if col in {
                "Department",
                "JobRole",
                "OverTime",
                "BusinessTravel",
                "MaritalStatus",
                "EducationField",
            }
            else "survival duration" if col == "YearsAtCompany"
            else "model feature"
            for col in df.columns
        ],
    }
)

render_dataframe(dictionary, title="Dataset Columns")

with st.expander("Prediction input columns", expanded=False):
    prediction_columns = [col for col in df.columns if col != "Attrition"]
    st.write(prediction_columns)

render_footer()
