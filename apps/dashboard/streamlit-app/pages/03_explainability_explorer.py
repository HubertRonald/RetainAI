from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.cards import kpi_grid  # noqa: E402
from components.layout import configure_page, render_footer, render_page_shell  # noqa: E402
from components.tables import render_dataframe  # noqa: E402
from modules.dashboard.explainability_charts import (  # noqa: E402
    interactive_feature_importance,
    interactive_shap_distribution,
    load_feature_importance,
    load_shap_values,
)
from modules.dashboard.explainability_loader import list_explainability_models  # noqa: E402

configure_page()

render_page_shell(
    title="Explainability Explorer",
    subtitle="Global model transparency and reusable SHAP artifacts",
    icon="explainability.svg",
    active_page="explainability",
    chips=[
        ("Source", "artifacts", "green"),
        ("Model", st.session_state.get("selected_model", "logistic_regression"), "purple"),
    ],
)

base = PROJECT_ROOT / "artifacts/explanations"
reports = PROJECT_ROOT / "artifacts/reports"

models = list_explainability_models(base)

if not models:
    st.warning("No explainability artifacts found.")
    render_footer()
    st.stop()

default_model = st.session_state.get("selected_model", models[0])
if default_model not in models:
    default_model = models[0]

model = st.selectbox(
    "Model",
    models,
    index=models.index(default_model),
    key="explainability_model_selector",
)

metadata_path = base / model / "metadata.json"
metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}

feature_importance_path = base / model / "feature_importance.parquet"
shap_values_path = base / model / "shap_values.joblib"

importance_df = load_feature_importance(feature_importance_path)
shap_values = load_shap_values(shap_values_path)

feature_names = []
if not importance_df.empty:
    feature_col = "feature" if "feature" in importance_df.columns else importance_df.columns[0]
    feature_names = importance_df[feature_col].astype(str).tolist()

kpi_grid(
    [
        {"label": "Model", "value": model, "helper": "Selected explainer", "accent": "#8b5cf6", "svg_icon": "model.svg"},
        {"label": "Samples", "value": metadata.get("n_samples", "N/A"), "helper": "Explained records", "accent": "#60a5fa", "svg_icon": "data.svg"},
        {"label": "Features", "value": metadata.get("n_features", len(feature_names) if feature_names else "N/A"), "helper": "Transformed feature space", "accent": "#22c55e", "svg_icon": "explainability.svg"},
    ]
)

tabs = st.tabs(["Global Importance", "SHAP Distribution", "Top Drivers Table", "Report"])

with tabs[0]:
    st.plotly_chart(interactive_feature_importance(importance_df, top_n=20), use_container_width=True)
    st.caption("Interactive ranking based on mean absolute SHAP values when available.")

with tabs[1]:
    if shap_values is not None and feature_names:
        st.plotly_chart(interactive_shap_distribution(shap_values, feature_names=feature_names, top_n=20), use_container_width=True)
        st.caption("Interactive distribution of SHAP values by feature. This is an interactive alternative to the static beeswarm artifact.")
    else:
        st.info("SHAP values or feature names are missing. Re-run the explainability pipeline to generate shap_values.joblib and feature_importance.parquet.")

with tabs[2]:
    if not importance_df.empty:
        render_dataframe(importance_df, title="Feature Importance Artifact", max_rows=30)
    else:
        st.info("Feature importance artifact not found.")

with tabs[3]:
    report_path = reports / f"explainability_report_{model}.md"
    fallback_report = reports / "explainability_report.md"

    if report_path.exists():
        st.markdown(report_path.read_text(encoding="utf-8"))
    elif fallback_report.exists():
        st.markdown(fallback_report.read_text(encoding="utf-8"))
    else:
        st.info("Explainability report not found.")

st.markdown(
    """
    <div class="retainai-explanation-note">
        <strong>Practical note:</strong>
        global explainability explains the model. For an employee-specific explanation,
        use Prediction Center, run a prediction, select a row and inspect row-level drivers.
    </div>
    """,
    unsafe_allow_html=True,
)

render_footer()
