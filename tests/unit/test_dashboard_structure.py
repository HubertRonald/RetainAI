from pathlib import Path


def test_dashboard_foundation_structure_exists() -> None:
    required_paths = [
        "apps/dashboard/streamlit-app",
        "apps/dashboard/streamlit-app/pages",
        "services/api",
        "services/dashboard",
        "services/compose.yaml",
        "modules/dashboard",
        "modules/api",
        "modules/connectors",
        "src/retainai/dashboard",
        "src/retainai/api",
        "docs/dashboard",
    ]
    for item in required_paths:
        assert Path(item).exists(), f"Missing dashboard structure path: {item}"
