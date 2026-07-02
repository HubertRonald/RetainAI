from __future__ import annotations

from pathlib import Path


def test_data_dictionary_page_exists() -> None:
    assert Path("apps/dashboard/streamlit-app/pages/05_data_dictionary.py").exists()


def test_data_dictionary_is_linked_from_sidebar() -> None:
    text = Path("apps/dashboard/streamlit-app/components/layout.py").read_text(
        encoding="utf-8"
    )
    assert "05_data_dictionary.py" in text
    assert "Data Dictionary" in text
