from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

KAGGLE_DATASET = "pavansubhasht/ibm-hr-analytics-attrition-dataset"


def validate_kaggle_cli() -> None:
    if shutil.which("kaggle") is None:
        raise RuntimeError(
            "Kaggle CLI was not found. Install it with `pip install kaggle`."
        )


def validate_kaggle_credentials() -> None:
    credentials = Path.home() / ".kaggle" / "kaggle.json"
    if not credentials.exists():
        raise FileNotFoundError(
            "Kaggle credentials not found at ~/.kaggle/kaggle.json. "
            "Create an API token from your Kaggle account settings."
        )


def download_ibm_hr_dataset(output_dir: str | Path) -> Path:
    validate_kaggle_cli()
    validate_kaggle_credentials()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    command = [
        "kaggle",
        "datasets",
        "download",
        "-d",
        KAGGLE_DATASET,
        "-p",
        str(output_path),
        "--unzip",
    ]

    subprocess.run(command, check=True)
    return output_path
