from __future__ import annotations

from modules.eda.attrition import (
    attrition_rate_by_category,
    attrition_rate_by_numeric_bins,
)
from modules.eda.correlations import target_numeric_correlation
from modules.eda.missingness import (
    has_missing_values,
    missing_summary,
    missingness_correlation,
    shadow_matrix,
)
from modules.eda.profiling import (
    categorical_profile,
    column_profile,
    dataset_overview,
    numeric_profile,
)
from modules.eda.quality import constant_columns, target_distribution


def test_dataset_overview(sample_hr_df) -> None:
    overview = dataset_overview(sample_hr_df)
    assert set(overview["metric"]) == {"rows", "columns", "duplicated_rows"}


def test_profiles(sample_hr_df) -> None:
    assert len(column_profile(sample_hr_df)) == sample_hr_df.shape[1]
    assert not numeric_profile(sample_hr_df).empty
    assert not categorical_profile(sample_hr_df).empty


def test_missingness_helpers(sample_hr_df) -> None:
    assert has_missing_values(sample_hr_df) is False
    assert missing_summary(sample_hr_df)["missing_count"].sum() == 0
    assert shadow_matrix(sample_hr_df).shape == sample_hr_df.shape
    assert missingness_correlation(sample_hr_df).empty


def test_quality_helpers(sample_hr_df) -> None:
    assert "EmployeeCount" in constant_columns(sample_hr_df)
    assert set(target_distribution(sample_hr_df)["target_value"]) == {"Yes", "No"}


def test_attrition_helpers(sample_hr_df) -> None:
    assert (
        "attrition_rate_pct"
        in attrition_rate_by_category(sample_hr_df, "OverTime").columns
    )
    assert (
        "attrition_rate_pct"
        in attrition_rate_by_numeric_bins(sample_hr_df, "MonthlyIncome", bins=2).columns
    )


def test_target_numeric_correlation(sample_hr_df) -> None:
    result = target_numeric_correlation(sample_hr_df)
    assert {"feature", "correlation"}.issubset(result.columns)
