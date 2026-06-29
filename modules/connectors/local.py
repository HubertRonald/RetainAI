from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


class LocalConnector:
    def __init__(self, project_root: str | Path = ".") -> None:
        self.project_root = Path(project_root).resolve()

    def resolve(self, relative_path: str | Path) -> Path:
        return self.project_root / relative_path

    def exists(self, relative_path: str | Path) -> bool:
        return self.resolve(relative_path).exists()

    def read_csv(self, relative_path: str | Path) -> pd.DataFrame:
        path = self.resolve(relative_path)
        if not path.exists():
            raise FileNotFoundError(f"Local file not found: {path}")
        return pd.read_csv(path)

    def read_markdown(self, relative_path: str | Path) -> str:
        path = self.resolve(relative_path)
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def read_json(self, relative_path: str | Path) -> dict:
        path = self.resolve(relative_path)
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
