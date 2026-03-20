"""Standard run summary report generation."""

from __future__ import annotations

from datetime import datetime, timezone

from perditio.files import atomic_write


def write_last_run(path: str, data: dict) -> None:
    """Write standard LAST_RUN.md format."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# Last Run",
        f"- timestamp: {now}",
    ]
    for key, value in data.items():
        lines.append(f"- {key}: {value}")
    atomic_write(path, "\n".join(lines) + "\n")
