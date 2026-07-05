from __future__ import annotations

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


def build_model(model_name: str, random_state: int = 42):
    if model_name == "logistic_regression":
        return LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=random_state,
        )

    if model_name == "random_forest":
        return RandomForestClassifier(
            n_estimators=300,
            class_weight="balanced",
            random_state=random_state,
            n_jobs=-1,
        )

    if model_name == "xgboost":
        try:
            from xgboost import XGBClassifier
        except Exception as exc:  # noqa: BLE001
            raise ImportError(
                "XGBoost could not be imported. On macOS this usually means "
                "`libomp.dylib` is missing. Install it with `sudo port install libomp` "
                "or `brew install libomp`, or run training inside the DevContainer."
            ) from exc

        return XGBClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=4,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=random_state,
            n_jobs=-1,
        )

    raise ValueError(f"Unsupported model name: {model_name}")
