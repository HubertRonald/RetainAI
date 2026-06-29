from __future__ import annotations
import sys
from pathlib import Path
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[4]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from modules.dashboard.survival_loader import get_survival_figures  # noqa: E402

st.title("Survival Analytics")
st.caption("YearsAtCompany is used as a proxy duration in the public IBM HR dataset.")
figures = get_survival_figures(PROJECT_ROOT / "artifacts/figures/survival")

for label, path in figures.items():
    st.markdown(f"### {label.replace('_', ' ').title()}")
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.info(f"Missing figure: {path}")
