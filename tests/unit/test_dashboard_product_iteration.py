from __future__ import annotations

from pathlib import Path

from modules.dashboard.explainability_charts import interactive_feature_importance
from modules.dashboard.explanation_payloads import build_bedrock_ready_payload
from modules.dashboard.export import build_dashboard_snapshot_payload
from modules.dashboard.local_explanations import explain_prediction_row


def test_dashboard_product_modules_are_importable() -> None:
    assert callable(build_dashboard_snapshot_payload)
    assert callable(build_bedrock_ready_payload)
    assert callable(interactive_feature_importance)
    assert callable(explain_prediction_row)


def test_layout_resolves_model_chip_from_session_state() -> None:
    text = Path("apps/dashboard/streamlit-app/components/layout.py").read_text(
        encoding="utf-8"
    )
    assert "def resolve_chips" in text
    assert 'label.lower() == "model"' in text


def test_explainability_selector_has_unique_key() -> None:
    text = Path(
        "apps/dashboard/streamlit-app/pages/03_explainability_explorer.py"
    ).read_text(encoding="utf-8")
    assert 'key="explainability_model_selector"' in text


def test_brain_icon_exists() -> None:
    assert Path("apps/dashboard/streamlit-app/assets/icons/brain.svg").exists()
