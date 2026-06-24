from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from modules.io.storage import save_dataframe


def split_dataset(
        df: pd.DataFrame,
        target: str,
        train_size: float = 0.70,
        validation_size: float = 0.15,
        test_size: float = 0.15,
        random_state: int = 42,
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if round(train_size + validation_size + test_size, 6) != 1.0:
        raise ValueError("train_size + validation_size + test_size must equal 1.0")

    train_df, temp_df = train_test_split(
        df,
        train_size=train_size,
        random_state=random_state,
        stratify=df[target],
    )

    relative_validation_size = validation_size / (validation_size + test_size)

    validation_df, test_df = train_test_split(
        temp_df,
        train_size=relative_validation_size,
        random_state=random_state,
        stratify=temp_df[target],
    )

    return (
        train_df.reset_index(drop=True),
        validation_df.reset_index(drop=True),
        test_df.reset_index(drop=True),
    )


def save_splits(
        train_df: pd.DataFrame,
        validation_df: pd.DataFrame,
        test_df: pd.DataFrame,
        output_root: str | Path = "data",
    ) -> None:
    root = Path(output_root)

    save_dataframe(train_df, root / "train" / "ibm_hr_attrition_train.csv")
    save_dataframe(
        validation_df,
        root / "validation" / "ibm_hr_attrition_validation.csv",
    )
    save_dataframe(test_df, root / "test" / "ibm_hr_attrition_test.csv")
