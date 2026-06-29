from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[4]
st.title("Prediction Center")
sample_path = PROJECT_ROOT / "data/prediction_input/ibm_hr_attrition_prediction_sample.csv"

if sample_path.exists():
    st.download_button("Download prediction template", data=sample_path.read_bytes(), file_name="ibm_hr_attrition_prediction_sample.csv", mime="text/csv")
else:
    st.info("Prediction sample not found yet.")
uploaded = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])
if uploaded:
    suffix = Path(uploaded.name).suffix.lower()
    df = pd.read_csv(uploaded) if suffix == ".csv" else pd.read_excel(uploaded)
    st.success(f"Loaded {len(df)} rows.")
    st.dataframe(df.head(20), use_container_width=True)
    st.info("Prediction execution will be connected in the next implementation step.")
else:
    st.info("Upload a file to preview prediction input.")
