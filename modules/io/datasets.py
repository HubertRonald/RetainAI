from __future__ import annotations

from pathlib import Path

import pandas as pd


DEFAULT_DATASET_FILE = "WA_Fn-UseC_-HR-Employee-Attrition.csv"


def get_raw_dataset_path(
        raw_dir: str | Path = "data/raw/ibm_hr_attrition",
        file_name: str = DEFAULT_DATASET_FILE,
    ) -> Path:
    dataset_path = Path(raw_dir) / file_name

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {dataset_path}. "
            "Run `python -m retainai.data.download_ibm_hr` first."
        )

    return dataset_path


def load_ibm_hr_dataset(
        raw_dir: str | Path = "data/raw/ibm_hr_attrition",
        file_name: str = DEFAULT_DATASET_FILE,
    ) -> pd.DataFrame:
    dataset_path = get_raw_dataset_path(raw_dir=raw_dir, file_name=file_name)
    return pd.read_csv(dataset_path)
