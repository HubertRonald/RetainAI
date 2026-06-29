from __future__ import annotations

import os
from pathlib import Path

from modules.connectors.local import LocalConnector


def get_connector(project_root: str | Path = "."):
    runtime = os.getenv("RETAINAI_RUNTIME", "local").lower()
    if runtime in {"local", "api", "s3", "aws"}:
        return LocalConnector(project_root)
    return LocalConnector(project_root)
