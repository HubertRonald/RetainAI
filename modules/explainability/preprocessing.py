from __future__ import annotations

import numpy as np
import pandas as pd


def extract_pipeline_parts(pipeline):
    return pipeline.named_steps["preprocessor"], pipeline.named_steps["model"]


def transform_features(pipeline, X: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
    preprocessor, _ = extract_pipeline_parts(pipeline)
    transformed = preprocessor.transform(X)

    if hasattr(transformed, "toarray"):
        transformed = transformed.toarray()

    feature_names = preprocessor.get_feature_names_out().tolist()
    return transformed, feature_names


def sample_background(X, max_samples: int = 100, random_state: int = 42):
    if len(X) <= max_samples:
        return X
    rng = np.random.default_rng(random_state)
    idx = rng.choice(len(X), size=max_samples, replace=False)
    return X[idx]
