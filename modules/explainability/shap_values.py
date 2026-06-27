from __future__ import annotations

import numpy as np


def compute_shap_values(explainer, X):
    values = explainer.shap_values(X)

    if isinstance(values, list):
        return values[1]

    values = np.asarray(values)

    if values.ndim == 3:
        return values[:, :, 1]

    return values


def get_expected_value(explainer):
    expected = explainer.expected_value

    if isinstance(expected, (list, tuple)):
        return expected[1]

    expected = np.asarray(expected)

    if expected.ndim > 0 and expected.size > 1:
        return expected[1]

    return float(expected)
