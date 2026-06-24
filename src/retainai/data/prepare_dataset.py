from __future__ import annotations

from modules.io.datasets import load_ibm_hr_dataset
from modules.io.storage import save_dataframe
from modules.preprocessing.cleaning import clean_ibm_hr_dataset
from modules.preprocessing.schema import load_schema
from modules.preprocessing.splitting import save_splits, split_dataset
from modules.preprocessing.validation import validate_schema


def main() -> None:
    schema = load_schema("configs/schema/ibm_hr_attrition.yaml")

    df = load_ibm_hr_dataset()
    report = validate_schema(df, schema)

    if not report.is_valid:
        message = "\n".join(report.errors)
        raise ValueError(f"Dataset validation failed:\n{message}")

    for warning in report.warnings:
        print(f"WARNING: {warning}")

    cleaned = clean_ibm_hr_dataset(df)

    save_dataframe(cleaned, "data/processed/ibm_hr_attrition_processed.csv")

    train_df, validation_df, test_df = split_dataset(
        cleaned,
        target=schema["target"],
        train_size=0.70,
        validation_size=0.15,
        test_size=0.15,
        random_state=42,
    )

    save_splits(train_df, validation_df, test_df)

    print("Dataset preparation completed successfully.")
    print(f"Processed shape: {cleaned.shape}")
    print(f"Train shape: {train_df.shape}")
    print(f"Validation shape: {validation_df.shape}")
    print(f"Test shape: {test_df.shape}")


if __name__ == "__main__":
    main()
