"""Tests for the speakup.skeleton module."""

from typing import Generator

import pytest

from speakup.skeleton import run


def test_run(capsys: Generator[pytest.CaptureFixture[str], None, None]) -> None:
    """Test the run function."""
    run()
    captured = capsys.readouterr()
    assert "SpeakUp CLI" in captured.out
