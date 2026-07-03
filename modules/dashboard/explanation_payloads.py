from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


def build_bedrock_ready_payload(
    employee_record: dict[str, Any],
    prediction: dict[str, Any],
    drivers: pd.DataFrame,
    model_name: str,
    payload_version: str = "v0.1",
) -> dict[str, Any]:
    top_drivers = drivers.to_dict(orient="records") if not drivers.empty else []

    return {
        "payload_type": "retainai_employee_retention_explanation",
        "payload_version": payload_version,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "model": {
            "name": model_name,
            "task": "employee_attrition_prediction",
        },
        "prediction": prediction,
        "employee_record": employee_record,
        "top_drivers": top_drivers,
        "intended_use": {
            "primary": "structured input for future Amazon Bedrock Retention Advisor",
            "notes": [
                "This payload is not sent to Bedrock currently",
                "It is designed to be consumed by a future retention advisory layer.",
                "It should not be interpreted as an automated HR decision.",
            ],
        },
    }


def payload_to_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False, default=str)


def save_payload(payload: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload_to_json(payload), encoding="utf-8")
    return path
