import os
import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def clean_env():
    """Clears all environment variables before each settings test."""
    with patch.dict(os.environ, {}, clear=True):
        yield
