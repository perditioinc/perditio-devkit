"""Tests for perditio.report module."""

import os
import tempfile

from perditio.report import write_last_run


def test_write_last_run():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as f:
        path = f.name

    try:
        write_last_run(path, {"repos_synced": 826, "duration": "20s"})
        with open(path) as f:
            content = f.read()
        assert "# Last Run" in content
        assert "repos_synced: 826" in content
        assert "duration: 20s" in content
        assert "timestamp:" in content
    finally:
        os.unlink(path)
