from __future__ import annotations

from modules.io.kaggle import download_ibm_hr_dataset


def main() -> None:
    output_path = download_ibm_hr_dataset("data/raw/ibm_hr_attrition")
    print(f"IBM HR dataset downloaded to: {output_path}")


if __name__ == "__main__":
    main()
