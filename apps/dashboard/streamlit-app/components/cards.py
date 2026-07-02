from __future__ import annotations

import base64
import html
from pathlib import Path

import streamlit as st


APP_DIR = Path(__file__).resolve().parents[1]
ICONS_DIR = APP_DIR / "assets/icons"


def _svg_data_uri(name: str | None) -> str:
    if not name:
        return ""

    path = ICONS_DIR / name
    if not path.exists():
        return ""

    raw = path.read_text(encoding="utf-8")
    encoded = base64.b64encode(raw.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


def kpi_card(
    label: str,
    value: str | int | float,
    helper: str = "",
    icon: str = "●",
    accent: str = "#615fff",
    svg_icon: str | None = None,
) -> None:
    svg_uri = _svg_data_uri(svg_icon)

    icon_html = (
        f'<img src="{svg_uri}" width="28" height="28"/>'
        if svg_uri
        else f'<span style="font-size:1.45rem;">{html.escape(icon)}</span>'
    )

    st.markdown(
        f"""
        <div class="retainai-card retainai-kpi-card">
            <div class="retainai-kpi-icon" style="color:{accent};">
                {icon_html}
            </div>
            <div>
                <div class="retainai-kpi-label">{html.escape(label)}</div>
                <div class="retainai-kpi-value">{html.escape(str(value))}</div>
                <div class="retainai-kpi-help" style="color:{accent};">{html.escape(helper)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_tip(message: str) -> None:
    st.markdown(
        f"""
        <div class="retainai-card" style="margin-top:1rem;">
            <span class="retainai-chip purple">Tip</span>
            <span style="margin-left:.5rem;color:#cbd5e1;">{html.escape(message)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_card(title: str, rows: dict[str, str]) -> None:
    rows_html = "".join(
        f"""
        <div class="retainai-status-row">
            <span>{html.escape(label)}</span>
            <span>{html.escape(value)}</span>
        </div>
        """
        for label, value in rows.items()
    )

    st.markdown(
        f"""
        <div class="retainai-card">
            <strong>{html.escape(title)}</strong>
            {rows_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
