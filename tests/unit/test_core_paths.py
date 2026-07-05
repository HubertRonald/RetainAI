from __future__ import annotations

from pathlib import Path

from retainai.core import paths


def test_core_paths_are_path_objects() -> None:
    assert isinstance(paths.PROJECT_ROOT, Path)
    assert isinstance(paths.DATA_DIR, Path)
    assert isinstance(paths.RAW_DATA_DIR, Path)
