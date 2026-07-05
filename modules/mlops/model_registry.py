from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def build_model_version_record(
    model_name: str,
    model_path: str | Path,
    metrics: dict[str, Any],
    run_id: str | None = None,
    experiment_name: str | None = None,
    registered_model_name: str | None = None,
) -> dict[str, Any]:
    return {
        "model_name": model_name,
        "registered_model_name": registered_model_name,
        "run_id": run_id,
        "experiment_name": experiment_name,
        "model_path": str(model_path),
        "metrics": metrics,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }


def update_model_registry_manifest(
    record: dict[str, Any],
    registry_path: str | Path = "artifacts/models/model_registry.json",
) -> Path:
    path = Path(registry_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        registry = json.loads(path.read_text(encoding="utf-8"))
    else:
        registry = {"models": {}, "latest": {}}

    model_name = record["model_name"]
    registry["models"].setdefault(model_name, [])
    registry["models"][model_name].append(record)
    registry["latest"][model_name] = record

    path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    return path


def load_model_registry_manifest(
    registry_path: str | Path = "artifacts/models/model_registry.json",
) -> dict[str, Any]:
    path = Path(registry_path)
    if not path.exists():
        return {"models": {}, "latest": {}}
    return json.loads(path.read_text(encoding="utf-8"))
