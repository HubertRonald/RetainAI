from __future__ import annotations

from modules.dashboard.charts import (
    COLOR_MAP,
    attrition_by_category,
    attrition_distribution,
    attrition_rate_by_category,
    histogram_by_attrition,
)


def test_dashboard_chart_public_functions_are_importable() -> None:
    assert COLOR_MAP["No"] == "#2f7df6"
    assert COLOR_MAP["Yes"] == "#ec4899"
    assert callable(attrition_distribution)
    assert callable(attrition_by_category)
    assert callable(attrition_rate_by_category)
    assert callable(histogram_by_attrition)
