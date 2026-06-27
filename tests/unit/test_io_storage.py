from __future__ import annotations

import pandas as pd
import pytest

from modules.io.storage import load_dataframe, save_dataframe


def test_save_and_load_csv_roundtrip(tmp_path) -> None:
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    path = tmp_path / "sample.csv"
    save_dataframe(df, path)
    loaded = load_dataframe(path)
    pd.testing.assert_frame_equal(df, loaded)


def test_save_dataframe_rejects_unsupported_extension(tmp_path) -> None:
    with pytest.raises(ValueError):
        save_dataframe(pd.DataFrame({"a": [1]}), tmp_path / "sample.txt")


def test_load_dataframe_rejects_missing_file(tmp_path) -> None:
    with pytest.raises(FileNotFoundError):
        load_dataframe(tmp_path / "missing.csv")
