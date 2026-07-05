from __future__ import annotations

import numpy as np
import pandas as pd


def shap_feature_importance(shap_values, feature_names: list[str]) -> pd.DataFrame:
    importance = np.abs(shap_values).mean(axis=0)

    return (
        pd.DataFrame(
            {
                "feature": feature_names,
                "mean_abs_shap": importance,
            }
        )
        .sort_values("mean_abs_shap", ascending=False)
        .reset_index(drop=True)
    )
