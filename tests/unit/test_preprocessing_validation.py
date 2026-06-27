from __future__ import annotations

import pandas as pd

from modules.preprocessing.cleaning import clean_ibm_hr_dataset
from modules.preprocessing.validation import (
    validate_duplicate_rows,
    validate_required_columns,
    validate_schema,
    validate_target_column,
)


def test_validate_required_columns_detects_missing(sample_hr_df) -> None:
    errors = validate_required_columns(sample_hr_df, ["Age", "MissingColumn"])
    assert errors == ["Missing required column: MissingColumn"]


def test_validate_target_column_accepts_allowed_values(sample_hr_df) -> None:
    assert validate_target_column(sample_hr_df, "Attrition", ["Yes", "No"]) == []


def test_validate_schema_returns_valid_report(sample_hr_df, minimal_schema) -> None:
    report = validate_schema(sample_hr_df, minimal_schema)
    assert report.is_valid is True
    assert report.errors == []


def test_validate_duplicate_rows_detects_duplicates(sample_hr_df) -> None:
    df = pd.concat([sample_hr_df, sample_hr_df.iloc[[0]]], ignore_index=True)
    assert validate_duplicate_rows(df) == ["Duplicated rows found: 1"]


def test_clean_ibm_hr_dataset_removes_duplicates(sample_hr_df) -> None:
    df = pd.concat([sample_hr_df, sample_hr_df.iloc[[0]]], ignore_index=True)
    cleaned = clean_ibm_hr_dataset(df)
    assert cleaned.duplicated().sum() == 0
