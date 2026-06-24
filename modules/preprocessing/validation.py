from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class ValidationReport:
    dataset_name: str
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def validate_required_columns(
        df: pd.DataFrame,
        required_columns: list[str],
    ) -> list[str]:
    missing = [column for column in required_columns if column not in df.columns]
    return [f"Missing required column: {column}" for column in missing]


def validate_target_column(
        df: pd.DataFrame,
        target: str,
        allowed_values: list[str] | None = None,
    ) -> list[str]:
    errors: list[str] = []

    if target not in df.columns:
        return [f"Target column not found: {target}"]

    if allowed_values is not None:
        observed_values = set(df[target].dropna().unique())
        invalid_values = observed_values.difference(set(allowed_values))

        if invalid_values:
            errors.append(
                f"Invalid target values found: {sorted(invalid_values)}. "
                f"Allowed values: {allowed_values}"
            )

    return errors


def validate_duplicate_rows(df: pd.DataFrame) -> list[str]:
    duplicated = int(df.duplicated().sum())
    if duplicated > 0:
        return [f"Duplicated rows found: {duplicated}"]
    return []


def validate_schema(df: pd.DataFrame, schema: dict) -> ValidationReport:
    errors: list[str] = []
    warnings: list[str] = []

    dataset_name = schema.get("dataset", "unknown")

    errors.extend(
        validate_required_columns(
            df=df,
            required_columns=schema.get("required_columns", []),
        )
    )

    errors.extend(
        validate_target_column(
            df=df,
            target=schema.get("target", "Attrition"),
            allowed_values=schema.get("target_values"),
        )
    )

    warnings.extend(validate_duplicate_rows(df))

    return ValidationReport(
        dataset_name=dataset_name,
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )
