"""Badge generation with suite tagging for Perditio projects."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import quote

SUITE_COLORS = {
    "Reporium": "6e40c9",
    "Perditio": "e85d04",
}

BADGE_START = "<!-- perditio-badges-start -->"
BADGE_END = "<!-- perditio-badges-end -->"


@dataclass
class BadgeBlock:
    repo: str
    workflow: Optional[str] = None
    suite: Optional[str] = None
    metrics: dict = field(default_factory=dict)
    python_version: str = "3.11+"

    def _shield(self, label: str, value: str, color: str) -> str:
        label_encoded = quote(label, safe="")
        value_encoded = quote(str(value), safe="")
        return f"![{label}](https://img.shields.io/badge/{label_encoded}-{value_encoded}-{color})"

    def render(self) -> str:
        lines = [BADGE_START]

        # Workflow badge
        if self.workflow:
            owner_repo = self.repo
            lines.append(
                f"[![Tests](https://github.com/{owner_repo}/actions/workflows/{self.workflow}"
                f"/badge.svg)](https://github.com/{owner_repo}/actions/workflows/{self.workflow})"
            )

        # Last commit
        lines.append(
            f"![Last Commit](https://img.shields.io/github/last-commit/{self.repo})"
        )

        # License
        lines.append(
            f"![License](https://img.shields.io/github/license/{self.repo})"
        )

        # Python version
        lines.append(self._shield("python", self.python_version, "3776ab"))

        # Suite badge
        if self.suite and self.suite in SUITE_COLORS:
            lines.append(self._shield("suite", self.suite, SUITE_COLORS[self.suite]))

        # Metric badges
        for label, value in self.metrics.items():
            lines.append(self._shield(label, value, "informational"))

        lines.append(BADGE_END)
        return "\n".join(lines)

    def update_readme(self, readme_path: str) -> bool:
        """Update badge block in existing README. Returns True if changed."""
        with open(readme_path, encoding="utf-8") as f:
            content = f.read()

        new_block = self.render()

        if BADGE_START in content and BADGE_END in content:
            pattern = re.compile(
                re.escape(BADGE_START) + r".*?" + re.escape(BADGE_END),
                re.DOTALL,
            )
            updated = pattern.sub(new_block, content)
        else:
            # Insert after first heading
            m = re.match(r"(#[^\n]*\n)", content)
            if m:
                updated = content[: m.end()] + "\n" + new_block + "\n" + content[m.end() :]
            else:
                updated = new_block + "\n\n" + content

        if updated == content:
            return False

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated)
        return True
