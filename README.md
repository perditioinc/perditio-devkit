# perditio-devkit

<!-- perditio-badges-start -->
[![Tests](https://github.com/perditioinc/perditio-devkit/actions/workflows/test.yml/badge.svg)](https://github.com/perditioinc/perditio-devkit/actions/workflows/test.yml)
![Last Commit](https://img.shields.io/github/last-commit/perditioinc/perditio-devkit)
![License](https://img.shields.io/github/license/perditioinc/perditio-devkit)
![python](https://img.shields.io/badge/python-3.11%2B-3776ab)
![suite](https://img.shields.io/badge/suite-Perditio-e85d04)
<!-- perditio-badges-end -->

Shared tooling for all Perditio projects. Pip-installable. Used by every repo in the Reporium suite.

## Install

```bash
pip install git+https://github.com/perditioinc/perditio-devkit.git
```

## Modules

### `perditio.badges` — Badge generation with suite tagging

```python
from perditio.badges import BadgeBlock

badges = BadgeBlock(
    repo="perditioinc/reporium-db",
    workflow="sync.yml",
    suite="Reporium",
    metrics={"repos tracked": "826", "languages": "29"},
)

# Render markdown badge block
print(badges.render())

# Update badge block in existing README (finds markers and replaces)
badges.update_readme("README.md")
```

### `perditio.github` — Async GitHub API client

```python
from perditio.github import GitHubClient

client = GitHubClient(token=os.getenv("GH_TOKEN"))
repo = await client.get_repo("perditioinc/reporium-db")
content = await client.get_file_content("perditioinc/reporium-db", "data/index.json")
```

### `perditio.files` — Atomic file write helpers

```python
from perditio.files import atomic_write, update_badge_value

atomic_write("output.json", json.dumps(data))
update_badge_value("README.md", "repos tracked", "826")
```

### `perditio.report` — Standard run summary

```python
from perditio.report import write_last_run

write_last_run("LAST_RUN.md", {"repos_synced": 826, "duration": "20s"})
```

## Suite Tagging

Repos in the Reporium suite get a purple `Reporium` badge. Perditio platform repos get an orange `Perditio` badge. This is controlled by the `suite` parameter in `BadgeBlock`.

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -v
ruff check perditio/ tests/
```
