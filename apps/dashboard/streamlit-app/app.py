from __future__ import annotations

import os
import sys
from pathlib import Path
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.layout import configure_page, render_header, render_status_strip  # noqa: E402

configure_page()
render_header()
runtime = os.getenv("RETAINAI_DASHBOARD_MODE", "local")
model = st.sidebar.selectbox("Model", ["logistic_regression", "random_forest", "xgboost"])
st.sidebar.markdown("---")
st.sidebar.caption("Runtime mode")
st.sidebar.code(runtime)
render_status_strip(runtime=runtime, model=model)
st.markdown("""
## Dashboard Foundation
Use the pages sidebar to navigate across Executive Overview, Prediction Center, Explainability Explorer and Survival Analytics.
""")
