from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def _safe_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9_.-]+", "_", value)
    return value.strip("_") or "payload"


def save_explanation_payload_sample(
    payload: dict[str, Any],
    output_dir: str | Path = "artifacts/explanations/samples",
    prefix: str = "employee",
    row_id: int | str | None = None,
) -> Path:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    suffix = f"row_{row_id}" if row_id is not None else timestamp
    filename = f"{_safe_name(prefix)}_{_safe_name(str(suffix))}.json"

    path = output / filename
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    return path


def list_payload_samples(
    input_dir: str | Path = "artifacts/explanations/samples",
) -> list[Path]:
    path = Path(input_dir)
    if not path.exists():
        return []
    return sorted(path.glob("*.json"))
