from __future__ import annotations

import pandas as pd
from lifelines import CoxPHFitter


def fit_cox_ph(
        cox_df: pd.DataFrame,
        duration_col: str = "duration",
        event_col: str = "event",
        penalizer: float = 0.1,
    ) -> CoxPHFitter:
    model = CoxPHFitter(penalizer=penalizer)
    model.fit(
        cox_df,
        duration_col=duration_col,
        event_col=event_col,
    )
    return model


def hazard_ratio_summary(model: CoxPHFitter) -> pd.DataFrame:
    summary = model.summary.reset_index()
    summary = summary.rename(columns={"covariate": "feature"})

    keep_columns = [
        "feature",
        "coef",
        "exp(coef)",
        "p",
        "coef lower 95%",
        "coef upper 95%",
    ]

    available_columns = [col for col in keep_columns if col in summary.columns]
    return summary[available_columns].sort_values("exp(coef)", ascending=False)
