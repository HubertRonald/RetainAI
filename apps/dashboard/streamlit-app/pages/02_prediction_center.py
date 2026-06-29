from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.cards import kpi_card  # noqa: E402
from components.layout import configure_page, render_footer, render_page_shell  # noqa: E402
from modules.dashboard.inference import explain_linear_prediction, load_model, predict_dataframe  # noqa: E402

configure_page()

selected_model = st.session_state.get("selected_model", "logistic_regression")

render_page_shell(
    title="Prediction Center",
    subtitle="Upload employee records, score attrition risk and inspect row-level drivers",
    icon="prediction.svg",
    active_page="prediction",
    chips=[("Mode", "local inference", "green"), ("Model", selected_model, "purple")],
)

sample_path = PROJECT_ROOT / "data/prediction_input/ibm_hr_attrition_prediction_sample.csv"
model_path = PROJECT_ROOT / "artifacts/models" / f"{selected_model}.pkl"

top_left, top_mid, top_right = st.columns([1, 1.4, 1])

with top_left:
    st.markdown('<div class="retainai-card">', unsafe_allow_html=True)
    st.markdown("### Template")
    if sample_path.exists():
        st.download_button(
            label="Download prediction template",
            data=sample_path.read_bytes(),
            file_name="ibm_hr_attrition_prediction_sample.csv",
            mime="text/csv",
        )
    else:
        st.warning("Prediction sample not found.")
    st.markdown("</div>", unsafe_allow_html=True)

with top_mid:
    st.markdown('<div class="retainai-card">', unsafe_allow_html=True)
    st.markdown("### Upload")
    uploaded = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])
    st.markdown("</div>", unsafe_allow_html=True)

with top_right:
    st.markdown('<div class="retainai-card">', unsafe_allow_html=True)
    st.markdown("### Model")
    if model_path.exists():
        st.success(f"Loaded: {selected_model}")
    else:
        st.error(f"Missing model: {model_path.name}")
    st.markdown("</div>", unsafe_allow_html=True)

input_df: pd.DataFrame | None = None

if uploaded:
    suffix = Path(uploaded.name).suffix.lower()
    if suffix == ".csv":
        input_df = pd.read_csv(uploaded)
    else:
        input_df = pd.read_excel(uploaded)
elif sample_path.exists():
    with st.expander("Use demo prediction sample", expanded=False):
        if st.button("Load demo sample"):
            input_df = pd.read_csv(sample_path)

if input_df is None:
    st.info("Upload a file or load the demo sample to run predictions.")
    render_footer()
    st.stop()

st.markdown("### Input Preview")
st.dataframe(input_df.head(25), use_container_width=True)

if not model_path.exists():
    st.error("Model artifact not available. Train classification models first.")
    render_footer()
    st.stop()

pipeline = load_model(model_path)
bundle = predict_dataframe(input_df, pipeline)

if bundle.missing_columns:
    st.error("The uploaded file is missing required model columns.")
    st.write(bundle.missing_columns)
    with st.expander("Required columns"):
        st.write(bundle.required_columns)
    render_footer()
    st.stop()

results = bundle.output_df

high_risk = int((results["risk_level"] == "High").sum())
avg_probability = float(results["attrition_probability"].mean())
records = len(results)

m1, m2, m3 = st.columns(3)
with m1:
    kpi_card("Predicted High Risk", f"{high_risk:,}", "Rows above high-risk threshold", "⚠️", "#ef4444")
with m2:
    kpi_card("Average Risk Probability", f"{avg_probability:.2%}", "Mean predicted attrition probability", "📈", "#ec4899")
with m3:
    kpi_card("Records Predicted", f"{records:,}", "Scored rows", "🧾", "#60a5fa")

st.markdown("### Prediction Results")
st.dataframe(results, use_container_width=True)

st.download_button(
    "Download predictions",
    data=results.to_csv(index=False).encode("utf-8"),
    file_name="retainai_predictions.csv",
    mime="text/csv",
)

st.markdown("### Row-level Explanation")

row_index = st.selectbox(
    "Select row to explain",
    list(range(len(results))),
    format_func=lambda i: f"Row {i} — Risk: {results.iloc[i]['risk_level']} — Prob: {results.iloc[i]['attrition_probability']:.2%}",
)

required = bundle.required_columns
row_df = results.iloc[[row_index]][required]
explanation = explain_linear_prediction(row_df, pipeline)

if explanation.empty:
    st.info("No local explanation available for this model.")
else:
    st.markdown(
        """
        <div class="retainai-card">
            <strong>Practical interpretation:</strong>
            the table below shows the strongest feature contributions for the selected uploaded row.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(explanation, use_container_width=True)

render_footer()
