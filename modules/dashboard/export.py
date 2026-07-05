from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any

import pandas as pd


def build_dashboard_snapshot_payload(
    filters: dict[str, Any],
    kpis: dict[str, Any],
    row_count: int,
    source: str = "local",
) -> dict[str, Any]:
    return {
        "snapshot_type": "retainai_dashboard_filtered_snapshot",
        "generated_at": datetime.now(timezone(timedelta(hours=-5))).isoformat() + "Z",
        "source": source,
        "filters": filters,
        "kpis": kpis,
        "row_count": row_count,
    }


def dashboard_snapshot_to_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# RetainAI Dashboard Snapshot",
        "",
        f"Generated at: `{payload['generated_at']}`",
        f"Source: `{payload['source']}`",
        "",
        "## Filters",
        "",
    ]

    for key, value in payload["filters"].items():
        lines.append(f"- **{key}:** {value if value else 'All'}")

    lines.extend(["", "## KPIs", ""])

    for key, value in payload["kpis"].items():
        lines.append(f"- **{key}:** {value}")

    lines.extend(["", f"Rows in filtered segment: `{payload['row_count']}`", ""])

    return "\n".join(lines)


def dashboard_snapshot_to_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False)


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")
