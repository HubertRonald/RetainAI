from __future__ import annotations

import io
import zipfile
from typing import Any

import pandas as pd
from plotly.graph_objects import Figure

from modules.dashboard.export import (
    dashboard_snapshot_to_json,
    dashboard_snapshot_to_markdown,
    dataframe_to_csv_bytes,
)


def figure_to_image_bytes(fig: Figure, image_format: str = "png") -> bytes:
    try:
        return fig.to_image(format=image_format, scale=2)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            "Plotly visual export requires kaleido. "
            "Install the dashboard extra or run `python -m pip install kaleido==0.2.1`."
        ) from exc


def build_visual_dashboard_zip(
    figures: dict[str, Figure],
    snapshot_payload: dict[str, Any],
    filtered_df: pd.DataFrame,
    image_format: str = "png",
) -> bytes:
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "dashboard_snapshot.md",
            dashboard_snapshot_to_markdown(snapshot_payload),
        )
        archive.writestr(
            "dashboard_snapshot.json",
            dashboard_snapshot_to_json(snapshot_payload),
        )
        archive.writestr(
            "filtered_dashboard_data.csv",
            dataframe_to_csv_bytes(filtered_df),
        )

        for name, fig in figures.items():
            image_bytes = figure_to_image_bytes(fig, image_format=image_format)
            archive.writestr(f"figures/{name}.{image_format}", image_bytes)

    buffer.seek(0)
    return buffer.getvalue()
