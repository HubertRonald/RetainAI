from __future__ import annotations

import pytest

lifelines = pytest.importorskip("lifelines")

from modules.survival.kaplan_meier import (  # noqa: E402
    fit_kaplan_meier,
    survival_probabilities,
)
from modules.survival.preprocessing import (  # noqa: E402
    prepare_cox_features,
    prepare_survival_dataset,
)


@pytest.mark.survival
def test_prepare_survival_dataset(sample_hr_df) -> None:
    survival_df = prepare_survival_dataset(
        sample_hr_df,
        duration_col="YearsAtCompany",
        event_col="Attrition",
        positive_class="Yes",
        drop_columns=["EmployeeNumber", "EmployeeCount", "Over18", "StandardHours"],
    )

    assert "duration" in survival_df.columns
    assert "event" in survival_df.columns
    assert set(survival_df["event"].unique()) == {0, 1}


@pytest.mark.survival
def test_kaplan_meier_fit_and_probabilities(sample_hr_df) -> None:
    survival_df = prepare_survival_dataset(sample_hr_df)
    kmf = fit_kaplan_meier(survival_df)
    probabilities = survival_probabilities(kmf, times=[1, 2, 3])

    assert len(probabilities) == 3
    assert "survival_probability" in probabilities.columns


@pytest.mark.survival
def test_prepare_cox_features(sample_hr_df) -> None:
    survival_df = prepare_survival_dataset(sample_hr_df)
    cox_df = prepare_cox_features(survival_df)

    assert "duration" in cox_df.columns
    assert "event" in cox_df.columns
