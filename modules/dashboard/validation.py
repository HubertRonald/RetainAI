from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class ValidationResult:
    is_valid: bool
    missing_columns: list[str]
    available_columns: list[str]


def validate_columns(df: pd.DataFrame, required_columns: list[str]) -> ValidationResult:
    available = df.columns.tolist()
    missing = [c for c in required_columns if c not in available]
    return ValidationResult(len(missing) == 0, missing, available)


def validate_required_files(paths: list[str | Path]) -> dict[str, bool]:
    return {str(path): Path(path).exists() for path in paths}
