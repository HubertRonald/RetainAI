from __future__ import annotations

from modules.io.kaggle import download_ibm_hr_dataset
from retainai.core.paths import IBM_HR_DATASET_DIR, ensure_data_directories


def main() -> None:
    ensure_data_directories()
    output_path = download_ibm_hr_dataset(IBM_HR_DATASET_DIR)
    print(f"IBM HR dataset downloaded to: {output_path}")


if __name__ == "__main__":
    main()
