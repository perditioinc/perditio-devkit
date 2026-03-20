"""Tests for perditio.badges module."""

import os
import tempfile

from perditio.badges import BADGE_END, BADGE_START, BadgeBlock


def test_render_basic():
    bb = BadgeBlock(repo="perditioinc/test-repo", workflow="test.yml")
    result = bb.render()
    assert BADGE_START in result
    assert BADGE_END in result
    assert "test.yml" in result
    assert "last-commit" in result


def test_render_with_suite():
    bb = BadgeBlock(repo="perditioinc/test", suite="Reporium")
    result = bb.render()
    assert "6e40c9" in result
    assert "Reporium" in result


def test_render_with_metrics():
    bb = BadgeBlock(repo="perditioinc/test", metrics={"repos": "826"})
    result = bb.render()
    assert "repos" in result
    assert "826" in result


def test_update_readme_inserts():
    bb = BadgeBlock(repo="perditioinc/test", workflow="ci.yml")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("# My Repo\n\nSome content\n")
        path = f.name

    try:
        changed = bb.update_readme(path)
        assert changed
        with open(path) as f:
            content = f.read()
        assert BADGE_START in content
        assert BADGE_END in content
        assert "Some content" in content
    finally:
        os.unlink(path)


def test_update_readme_replaces():
    bb = BadgeBlock(repo="perditioinc/test", metrics={"v": "2"})
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write(f"# Repo\n\n{BADGE_START}\nold badges\n{BADGE_END}\n\nContent\n")
        path = f.name

    try:
        changed = bb.update_readme(path)
        assert changed
        with open(path) as f:
            content = f.read()
        assert "old badges" not in content
        assert "v" in content
        assert "Content" in content
    finally:
        os.unlink(path)
