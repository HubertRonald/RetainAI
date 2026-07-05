from __future__ import annotations

from modules.io.datasets import load_ibm_hr_dataset
from modules.preprocessing.schema import load_schema
from modules.preprocessing.validation import validate_schema
from retainai.core.paths import IBM_HR_SCHEMA_FILE


def main() -> None:
    schema = load_schema(IBM_HR_SCHEMA_FILE)
    df = load_ibm_hr_dataset()

    report = validate_schema(df, schema)

    print(f"Dataset: {report.dataset_name}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Valid: {report.is_valid}")

    if report.errors:
        print("\nErrors:")
        for error in report.errors:
            print(f"- {error}")

    if report.warnings:
        print("\nWarnings:")
        for warning in report.warnings:
            print(f"- {warning}")

    if not report.is_valid:
        raise SystemExit(1)

    print("\nDataset validation completed successfully.")


if __name__ == "__main__":
    main()
