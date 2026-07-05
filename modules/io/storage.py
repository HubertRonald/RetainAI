from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_dataframe(df: pd.DataFrame, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    elif output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    else:
        raise ValueError(f"Unsupported output format: {output_path.suffix}")

    return output_path


def load_dataframe(path: str | Path) -> pd.DataFrame:
    input_path = Path(path)

    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    if input_path.suffix == ".csv":
        return pd.read_csv(input_path)
    if input_path.suffix == ".parquet":
        return pd.read_parquet(input_path)

    raise ValueError(f"Unsupported input format: {input_path.suffix}")
