from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.layout import configure_page, render_footer, render_page_shell  # noqa: E402
from modules.dashboard.explainability_loader import get_explainability_figures, list_explainability_models  # noqa: E402

configure_page()

render_page_shell(
    title="Explainability Explorer",
    subtitle="Global model transparency and reusable SHAP artifacts",
    icon="explainability.svg",
    active_page="explainability",
    chips=[("Source", "artifacts", "green"), ("SHAP", "precomputed", "purple")],
)

base = PROJECT_ROOT / "artifacts/explanations"
figures = PROJECT_ROOT / "artifacts/figures/explainability"
reports = PROJECT_ROOT / "artifacts/reports"

models = list_explainability_models(base)

if not models:
    st.warning("No explainability artifacts found.")
    render_footer()
    st.stop()

default_model = st.session_state.get("selected_model", models[0])
if default_model not in models:
    default_model = models[0]

model = st.selectbox("Model", models, index=models.index(default_model))
paths = get_explainability_figures(figures, model)

metadata_path = base / model / "metadata.json"
metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="retainai-card">', unsafe_allow_html=True)
    st.metric("Model", model)
    st.markdown("</div>", unsafe_allow_html=True)
with c2:
    st.markdown('<div class="retainai-card">', unsafe_allow_html=True)
    st.metric("Samples", metadata.get("n_samples", "N/A"))
    st.markdown("</div>", unsafe_allow_html=True)
with c3:
    st.markdown('<div class="retainai-card">', unsafe_allow_html=True)
    st.metric("Features", metadata.get("n_features", "N/A"))
    st.markdown("</div>", unsafe_allow_html=True)

tabs = st.tabs(["Global Importance", "Beeswarm", "Local Example", "Report"])

with tabs[0]:
    path = paths["feature_importance"]
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.info(f"Missing figure: {path}")

with tabs[1]:
    path = paths["beeswarm"]
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.info(f"Missing figure: {path}")

with tabs[2]:
    path = paths["waterfall"]
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.info(f"Missing figure: {path}")

with tabs[3]:
    report_path = reports / f"explainability_report_{model}.md"
    if report_path.exists():
        st.markdown(report_path.read_text(encoding="utf-8"))
    else:
        st.info(f"Missing report: {report_path}")

st.info("For practical prediction explanations, use Prediction Center and select a row after scoring uploaded records.")
render_footer()
