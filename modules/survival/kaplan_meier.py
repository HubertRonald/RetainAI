from __future__ import annotations

import pandas as pd
from lifelines import KaplanMeierFitter


def fit_kaplan_meier(
    survival_df: pd.DataFrame,
    duration_col: str = "duration",
    event_col: str = "event",
) -> KaplanMeierFitter:
    kmf = KaplanMeierFitter()
    kmf.fit(
        durations=survival_df[duration_col],
        event_observed=survival_df[event_col],
        label="Overall Survival",
    )
    return kmf


def survival_probabilities(
    kmf: KaplanMeierFitter,
    times: list[float],
) -> pd.DataFrame:
    rows = []

    for time in times:
        rows.append(
            {
                "time": time,
                "survival_probability": float(kmf.predict(time)),
            }
        )

    return pd.DataFrame(rows)


def fit_kaplan_meier_by_group(
    survival_df: pd.DataFrame,
    group_col: str,
    duration_col: str = "duration",
    event_col: str = "event",
) -> dict[str, KaplanMeierFitter]:
    models = {}

    for group_value, group_df in survival_df.groupby(group_col, dropna=False):
        kmf = KaplanMeierFitter()
        kmf.fit(
            durations=group_df[duration_col],
            event_observed=group_df[event_col],
            label=str(group_value),
        )
        models[str(group_value)] = kmf

    return models
