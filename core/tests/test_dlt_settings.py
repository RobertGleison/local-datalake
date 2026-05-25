import os
from unittest.mock import patch
from core.settings.dlt_settings import DLTSettings


def test_dlt_settings_defaults():
    """Verify that DLTSettings calculates logical worker counts based on threads."""
    with patch("os.cpu_count", return_value=8):
        settings = DLTSettings()

        assert settings.available_threads == 8
        assert settings.extract_workers == 7
        assert os.environ["EXTRACT__WORKERS"] == "7"
        assert settings.normalize_workers == 6
        assert os.environ["NORMALIZE__WORKERS"] == "6"
        assert settings.load_workers == 7
        assert os.environ["LOAD__WORKERS"] == "7"


def test_dlt_settings_env_overrides():
    """Verify that custom environment variables override defaults."""
    os.environ["EXTRACT__WORKERS"] = "12"
    os.environ["NORMALIZE__WORKERS"] = "8"
    os.environ["LOAD__WORKERS"] = "10"
    os.environ["DLT_DATA_DIR"] = "/tmp/dlt"

    with patch("os.cpu_count", return_value=4):
        settings = DLTSettings()

        assert settings.available_threads == 4
        assert settings.extract_workers == 12
        assert settings.normalize_workers == 8
        assert settings.load_workers == 10
        assert os.environ["EXTRACT__WORKERS"] == "12"
