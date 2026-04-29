"""Shared pytest configuration and fixtures."""

import sys
import logging
from pathlib import Path

import pytest

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

# Configure logging for tests
logging.basicConfig(level=logging.WARNING)


@pytest.fixture
def caplog_handler(caplog):
    """Fixture for capturing log output."""
    caplog.set_level(logging.DEBUG)
    return caplog


@pytest.fixture
def temp_data_dir(tmp_path):
    """Fixture for temporary data directory."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir
