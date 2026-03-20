"""Tests for perditio.files module."""

import os
import tempfile

from perditio.files import atomic_write, update_badge_value


def test_atomic_write():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        path = f.name

    try:
        atomic_write(path, "hello world")
        with open(path) as f:
            assert f.read() == "hello world"
        assert not os.path.exists(path + ".tmp")
    finally:
        os.unlink(path)


def test_update_badge_value():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".md") as f:
        f.write("![repos](https://img.shields.io/badge/repos-100-blue)\n")
        path = f.name

    try:
        changed = update_badge_value(path, "repos", "826")
        assert changed
        with open(path) as f:
            assert "826" in f.read()
    finally:
        os.unlink(path)


def test_update_badge_value_no_match():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".md") as f:
        f.write("# No badges here\n")
        path = f.name

    try:
        changed = update_badge_value(path, "repos", "826")
        assert not changed
    finally:
        os.unlink(path)
