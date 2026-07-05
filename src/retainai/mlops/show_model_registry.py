from __future__ import annotations

import json

from modules.mlops.model_registry import load_model_registry_manifest
from retainai.core.paths import PROJECT_ROOT


def main() -> None:
    registry = load_model_registry_manifest(
        PROJECT_ROOT / "artifacts/models/model_registry.json"
    )
    print(json.dumps(registry, indent=2))


if __name__ == "__main__":
    main()
