from __future__ import annotations

import pandas as pd
from lifelines.utils import concordance_index


def cox_concordance_index(
        df: pd.DataFrame,
        predicted_partial_hazard,
        duration_col: str = "duration",
        event_col: str = "event",
    ) -> float:
    return float(
        concordance_index(
            event_times=df[duration_col],
            predicted_scores=-predicted_partial_hazard,
            event_observed=df[event_col],
        )
    )
