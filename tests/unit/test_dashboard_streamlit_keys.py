from __future__ import annotations

from pathlib import Path


def test_sidebar_model_selector_has_unique_key() -> None:
    text = Path("apps/dashboard/streamlit-app/components/layout.py").read_text(
        encoding="utf-8"
    )
    assert 'key="sidebar_model_selector"' in text


def test_explainability_selector_has_unique_key() -> None:
    text = Path(
        "apps/dashboard/streamlit-app/pages/03_explainability_explorer.py"
    ).read_text(encoding="utf-8")
    assert 'key="explainability_model_selector"' in text
