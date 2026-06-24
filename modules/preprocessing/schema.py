from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_schema(schema_path: str | Path) -> dict[str, Any]:
    path = Path(schema_path)

    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)
