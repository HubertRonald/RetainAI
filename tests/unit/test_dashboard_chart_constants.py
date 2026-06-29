from __future__ import annotations

from modules.dashboard.charts import COLOR_MAP


def test_dashboard_attrition_color_map_is_available() -> None:
    assert COLOR_MAP["No"] == "#2f7df6"
    assert COLOR_MAP["Yes"] == "#ec4899"
