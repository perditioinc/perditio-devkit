"""Atomic file write and badge value update helpers."""

from __future__ import annotations

import os
import re


def atomic_write(path: str, content: str) -> None:
    """Write to .tmp file then os.replace() — never corrupts on failure."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp, path)


def update_badge_value(readme_path: str, badge_label: str, new_value: str) -> bool:
    """Update a single shields.io badge value in README. Returns True if changed."""
    with open(readme_path, encoding="utf-8") as f:
        content = f.read()

    escaped_label = re.escape(badge_label.replace(" ", "%20"))
    pattern = rf"(!\[{re.escape(badge_label)}\]\(https://img\.shields\.io/badge/{escaped_label}-)([^-]+)(-)"
    updated, count = re.subn(pattern, rf"\g<1>{new_value}\g<3>", content)

    if count == 0 or updated == content:
        return False

    atomic_write(readme_path, updated)
    return True
