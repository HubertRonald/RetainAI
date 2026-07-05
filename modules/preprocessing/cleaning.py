from __future__ import annotations

import pandas as pd


def clean_ibm_hr_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    # Keep raw column names for compatibility with Kaggle references.
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    return cleaned
