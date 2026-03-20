"""README update helpers."""

from __future__ import annotations

import re


def replace_section(content: str, section_name: str, new_content: str) -> str:
    """Replace content between section markers.

    Markers are HTML comments: <!-- section:NAME:start --> and <!-- section:NAME:end -->
    """
    start = f"<!-- section:{section_name}:start -->"
    end = f"<!-- section:{section_name}:end -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = f"{start}\n{new_content}\n{end}"
    return pattern.sub(replacement, content)


def update_inline_stat(content: str, label: str, value: str) -> str:
    """Update an inline stat like **818 repos** to a new value."""
    pattern = rf"\*\*[\d,]+\s+{re.escape(label)}\*\*"
    return re.sub(pattern, f"**{value} {label}**", content)
