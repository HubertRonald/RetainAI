from __future__ import annotations
import sys
from pathlib import Path
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[4]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from modules.dashboard.explainability_loader import get_explainability_figures, list_explainability_models  # noqa: E402

st.title("Explainability Explorer")
base = PROJECT_ROOT / "artifacts/explanations"
figures = PROJECT_ROOT / "artifacts/figures/explainability"
models = list_explainability_models(base)

if not models:
    st.warning("No explainability artifacts found.")
    st.stop()
model = st.selectbox("Model", models)
paths = get_explainability_figures(figures, model)

for label, path in paths.items():
    st.markdown(f"### {label.replace('_', ' ').title()}")
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.info(f"Missing figure: {path}")
