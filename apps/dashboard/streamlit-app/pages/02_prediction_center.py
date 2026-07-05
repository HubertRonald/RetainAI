from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.cards import kpi_grid  # noqa: E402
from components.layout import configure_page, render_footer, render_page_shell  # noqa: E402
from components.tables import render_dataframe  # noqa: E402
from modules.dashboard.explanation_payloads import (  # noqa: E402
    build_bedrock_ready_payload,
    payload_to_json,
)
from modules.dashboard.inference import load_model, predict_dataframe  # noqa: E402
from modules.dashboard.local_explanations import explain_prediction_row  # noqa: E402
from modules.dashboard.payload_store import save_explanation_payload_sample  # noqa: E402
from modules.dashboard.retention_advisor_prompts import build_retention_advisor_prompt  # noqa: E402
from modules.dashboard.api_client import RetainAIApiClient  # noqa: E402

configure_page()

selected_model = st.session_state.get("selected_model", "logistic_regression")
prediction_mode = os.getenv("RETAINAI_PREDICTION_MODE", "local").lower()

render_page_shell(
    title="Prediction Center",
    subtitle="Upload employee records, score attrition risk and inspect row-level drivers",
    icon="prediction.svg",
    active_page="prediction",
    chips=[
        ("Mode", prediction_mode, "green"),
        ("Model", selected_model, "purple"),
    ],
)

sample_path = PROJECT_ROOT / "data/prediction_input/ibm_hr_attrition_prediction_sample.csv"
model_path = PROJECT_ROOT / "artifacts/models" / f"{st.session_state.get('selected_model', selected_model)}.pkl"

top_left, top_mid, top_right = st.columns([1, 1.4, 1], gap="medium")

with top_left:
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

with top_mid:
    st.markdown("### Upload")
    uploaded = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"], key="prediction_upload")

with top_right:
    st.markdown("### Model")
    if model_path.exists():
        st.success(f"Loaded: {model_path.stem}")
    else:
        st.error(f"Missing model: {model_path.name}")

with st.expander("Use demo prediction sample", expanded=False):
    use_demo = st.button("Load demo sample", key="load_demo_prediction_sample")

input_df: pd.DataFrame | None = None

if uploaded:
    suffix = Path(uploaded.name).suffix.lower()
    if suffix == ".csv":
        input_df = pd.read_csv(uploaded)
    else:
        input_df = pd.read_excel(uploaded)
elif use_demo and sample_path.exists():
    input_df = pd.read_csv(sample_path)

if input_df is None:
    st.info("Upload a file or load the demo sample to run predictions.")
    render_footer()
    st.stop()

render_dataframe(input_df, title="Input Preview", max_rows=25)

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

if prediction_mode == "api":
    try:
        api_client = RetainAIApiClient()
        results = api_client.predict(bundle.input_df, model_name=model_path.stem)
        st.success("Predictions generated through RetainAI API.")
    except Exception as exc:  # noqa: BLE001
        st.warning(f"API prediction failed. Falling back to local mode. Details: {exc}")
        results = bundle.output_df
else:
    results = bundle.output_df

high_risk = int((results["risk_level"] == "High").sum())
avg_probability = float(results["attrition_probability"].mean())
records = len(results)

kpi_grid(
    [
        {
            "label": "Predicted High Risk",
            "value": f"{high_risk:,}",
            "helper": "Rows above high-risk threshold",
            "icon": "⚠️",
            "accent": "#ef4444",
            "svg_icon": "prediction.svg",
        },
        {
            "label": "Average Risk Probability",
            "value": f"{avg_probability:.2%}",
            "helper": "Mean predicted attrition probability",
            "icon": "📈",
            "accent": "#ec4899",
            "svg_icon": "overview.svg",
        },
        {
            "label": "Records Predicted",
            "value": f"{records:,}",
            "helper": "Scored rows",
            "icon": "🧾",
            "accent": "#60a5fa",
            "svg_icon": "data.svg",
        },
    ]
)

render_dataframe(results, title="Prediction Results")

csv_buffer = results.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download predictions",
    data=csv_buffer,
    file_name="retainai_predictions.csv",
    mime="text/csv",
)

st.markdown("### Row-level Explanation")

row_index = st.selectbox(
    "Select row to explain",
    list(range(len(results))),
    format_func=lambda i: (
        f"Row {i} — Risk: {results.iloc[i]['risk_level']} — "
        f"Prob: {results.iloc[i]['attrition_probability']:.2%}"
    ),
    key="prediction_row_explanation_selector",
)

required = bundle.required_columns
row_df = bundle.input_df.iloc[[row_index]][required]
background_df = bundle.input_df[required].head(min(len(bundle.input_df), 100))

try:
    explanation = explain_prediction_row(
        row_df=row_df,
        pipeline=pipeline,
        background_df=background_df,
        top_n=12,
    )
except Exception as exc:
    st.warning(f"Local explanation could not be generated: {exc}")
    explanation = pd.DataFrame()

if explanation.empty:
    st.info("No local explanation available for this row/model.")
else:
    st.markdown(
        """
        <div class="retainai-explanation-note">
            <strong>Practical interpretation:</strong>
            this table shows the strongest drivers for the selected uploaded row.
            For Logistic Regression, RetainAI uses linear feature contributions.
            For Random Forest and XGBoost, RetainAI uses row-level SHAP values.
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_dataframe(explanation)

    prediction_payload = {
        "prediction": int(results.iloc[row_index]["prediction"]),
        "attrition_probability": float(results.iloc[row_index]["attrition_probability"]),
        "risk_level": str(results.iloc[row_index]["risk_level"]),
    }

    payload = build_bedrock_ready_payload(
        employee_record=input_df.iloc[row_index].to_dict(),
        prediction=prediction_payload,
        drivers=explanation,
        model_name=model_path.stem,
    )

    payload_json = payload_to_json(payload)

    with st.expander("Bedrock-ready structured explanation payload", expanded=False):
        st.json(payload)
        st.download_button(
            "Download explanation payload JSON",
            data=payload_json.encode("utf-8"),
            file_name=f"retainai_explanation_row_{row_index}.json",
            mime="application/json",
        )
        
        if st.button("Persist payload sample locally", key="persist_explanation_payload"):
            saved_path = save_explanation_payload_sample(
                payload=payload,
                row_id=row_index,
                prefix=f"{model_path.stem}_employee",
            )
            st.success(f"Payload persisted to {saved_path}")
            
    with st.expander("Retention Advisor prompt preview", expanded=False):
        advisor_prompt = build_retention_advisor_prompt(payload)
        st.code(advisor_prompt, language="text")
        st.download_button(
            "Download Retention Advisor prompt",
            data=advisor_prompt.encode("utf-8"),
            file_name=f"retainai_retention_advisor_prompt_row_{row_index}.txt",
            mime="text/plain",
        )

render_footer()
