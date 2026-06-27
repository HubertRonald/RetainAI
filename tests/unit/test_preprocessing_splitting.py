from __future__ import annotations

import pandas as pd
import pytest

from modules.preprocessing.splitting import split_dataset


def test_split_dataset_returns_expected_total_rows() -> None:
    df = pd.DataFrame(
        {
            "Attrition": ["Yes", "No"] * 20,
            "Age": list(range(20, 60)),
            "MonthlyIncome": list(range(3000, 7000, 100)),
        }
    )

    train_df, validation_df, test_df = split_dataset(
        df,
        target="Attrition",
        train_size=0.5,
        validation_size=0.25,
        test_size=0.25,
        random_state=42,
    )

    assert len(train_df) + len(validation_df) + len(test_df) == len(df)
    assert set(train_df["Attrition"]) == {"Yes", "No"}
    assert set(validation_df["Attrition"]) == {"Yes", "No"}
    assert set(test_df["Attrition"]) == {"Yes", "No"}


def test_split_dataset_rejects_invalid_split_sum(sample_hr_df) -> None:
    with pytest.raises(ValueError):
        split_dataset(
            sample_hr_df,
            target="Attrition",
            train_size=0.8,
            validation_size=0.2,
            test_size=0.2,
        )
