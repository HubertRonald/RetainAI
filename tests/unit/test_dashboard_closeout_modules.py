from __future__ import annotations

from modules.dashboard.api_client import RetainAIApiClient
from modules.dashboard.payload_store import save_explanation_payload_sample
from modules.dashboard.retention_advisor_prompts import build_retention_advisor_messages
from modules.dashboard.visual_export import build_visual_dashboard_zip


def test_api_client_can_be_constructed() -> None:
    client = RetainAIApiClient(base_url="http://localhost:8001")
    assert client.base_url == "http://localhost:8001"


def test_retention_advisor_messages_are_generated() -> None:
    messages = build_retention_advisor_messages({"prediction": {"risk_level": "High"}})
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"


def test_payload_sample_can_be_saved(tmp_path) -> None:
    path = save_explanation_payload_sample(
        {"payload_type": "test"},
        output_dir=tmp_path,
        row_id=1,
    )
    assert path.exists()
    assert path.suffix == ".json"


def test_visual_export_function_is_importable() -> None:
    assert callable(build_visual_dashboard_zip)
