from __future__ import annotations

import base64
import html
import os
from datetime import datetime
from pathlib import Path

import streamlit as st


APP_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[4]
ASSETS_DIR = APP_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
STYLES_DIR = ASSETS_DIR / "styles"
LANDING_PAGE = "https://hubertronald.github.io/"

def configure_page() -> None:
    st.set_page_config(
        page_title="RetainAI",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def load_svg(name: str) -> str:
    path = ICONS_DIR / name
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def svg_data_uri(name: str) -> str:
    raw = load_svg(name)
    if not raw:
        return ""
    encoded = base64.b64encode(raw.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


def inject_global_styles() -> None:
    css_path = STYLES_DIR / "dashboard.css"
    css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_sidebar(active_page: str = "") -> None:
    runtime = os.getenv("RETAINAI_DASHBOARD_MODE", "local")
    api_url = os.getenv("RETAINAI_API_URL", "http://localhost:8001")
    model = st.session_state.get("selected_model", "logistic_regression")

    with st.sidebar:
        icon_uri = svg_data_uri("retainai.svg")

        st.markdown(
            f"""
            <div class="retainai-brand">
                <div class="retainai-brand-icon">
                    <img src="{icon_uri}" width="30" height="30"/>
                </div>
                <div>
                    <div class="retainai-brand-title">RetainAI</div>
                    <div class="retainai-brand-subtitle">Employee Retention Intelligence</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="retainai-nav-label">Navigation</div>', unsafe_allow_html=True)

        st.page_link("app.py", label="Home", icon=":material/home:")
        st.page_link(
            "pages/01_executive_overview.py",
            label="Executive Overview",
            icon=":material/dashboard:",
        )
        st.page_link(
            "pages/02_prediction_center.py",
            label="Prediction Center",
            icon=":material/target:",
        )
        st.page_link(
            "pages/03_explainability_explorer.py",
            label="Explainability Explorer",
            icon=":material/psychology:",
        )
        st.page_link(
            "pages/04_survival_analytics.py",
            label="Survival Analytics",
            icon=":material/timeline:",
        )

        dictionary_page = Path(__file__).resolve().parents[1] / "pages/05_data_dictionary.py"
        if dictionary_page.exists():
            st.page_link(
                "pages/05_data_dictionary.py",
                label="Data Dictionary",
                icon=":material/dictionary:",
            )

        st.markdown('<div class="retainai-nav-label">System</div>', unsafe_allow_html=True)

        st.session_state["selected_model"] = st.selectbox(
            "Model",
            ["logistic_regression", "random_forest", "xgboost"],
            index=["logistic_regression", "random_forest", "xgboost"].index(model),
            key="sidebar_model_selector",
        )

        st.markdown(
            f"""
            <div class="retainai-sidebar-card">
                <strong>System Status</strong>
                <div class="retainai-status-row">
                    <span>Runtime Mode</span>
                    <span class="retainai-status-badge green">{html.escape(runtime)}</span>
                </div>
                <div class="retainai-status-row">
                    <span>API URL</span>
                    <span class="retainai-status-badge">{html.escape(api_url.replace("http://", ""))}</span>
                </div>
                <div class="retainai-status-row">
                    <span>Model</span>
                    <span>{html.escape(st.session_state["selected_model"])}</span>
                </div>
                <div class="retainai-status-row">
                    <span>Last Update</span>
                    <span class="retainai-status-badge green">Just now</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="retainai-sidebar-card retainai-sidebar-footer-card">
                <div style="font-weight:700;color:#e2e8f0;">RetainAI Dashboard v0.3.0</div>
                <div style="color:#94a3b8;font-size:.78rem;margin-top:.3rem;">
                    Product dashboard foundation
                </div>
                <div style="margin-top:.9rem;color:#94a3b8;font-size:.78rem;">
                    Need help? Review dashboard docs.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def render_page_header(
        title: str,
        subtitle: str,
        icon: str = "overview.svg",
        chips: list[tuple[str, str, str]] | None = None,
    ) -> None:
    icon_uri = svg_data_uri(icon)
    chips = chips or []

    chip_html = "".join(
        f'<span class="retainai-chip {html.escape(color)}">{html.escape(label)}: <strong>{html.escape(value)}</strong></span>'
        for label, value, color in chips
    )

    st.markdown(
        f"""
        <div class="retainai-header">
            <div class="retainai-title-wrap">
                <div class="retainai-page-icon">
                    <img src="{icon_uri}" width="26" height="26"/>
                </div>
                <div>
                    <h1>{html.escape(title)}</h1>
                    <p>{html.escape(subtitle)}</p>
                </div>
            </div>
            <div class="retainai-toolbar">{chip_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    year = datetime.now().year
    st.markdown(
        f"""
        <div class="retainai-footer">
            <p>
                Coded with
                <a href="{LANDING_PAGE}" target="_blank" class="footer-heart">♥</a>
                by
                <a href="{LANDING_PAGE}" target="_blank">Hubert Ronald</a>
                <br>
                © Copyright {year}
                <a href="{LANDING_PAGE}" target="_blank">[-] Liasoft</a>
                - All Rights Reserved
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_shell(
        title: str,
        subtitle: str,
        icon: str = "overview.svg",
        active_page: str = "",
        chips: list[tuple[str, str, str]] | None = None,
    ) -> None:
    inject_global_styles()
    render_sidebar(active_page=active_page)
    render_page_header(title=title, subtitle=subtitle, icon=icon, chips=chips)
