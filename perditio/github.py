"""Shared async GitHub API client with retry and rate limit handling."""

from __future__ import annotations

import asyncio
import base64
import logging
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com"


class GitHubClient:
    """Async GitHub API client with retry, rate limit handling, and semaphore concurrency."""

    def __init__(self, token: str, concurrency: int = 10, max_retries: int = 3):
        self.token = token
        self.semaphore = asyncio.Semaphore(concurrency)
        self.max_retries = max_retries

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        async with self.semaphore:
            for attempt in range(self.max_retries):
                try:
                    async with httpx.AsyncClient(timeout=30) as client:
                        resp = await client.request(method, url, headers=self._headers(), **kwargs)
                    if resp.status_code == 403 and "rate limit" in resp.text.lower():
                        wait = min(2 ** attempt * 10, 60)
                        logger.warning("Rate limited, waiting %ds", wait)
                        await asyncio.sleep(wait)
                        continue
                    return resp
                except httpx.TimeoutException:
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                    else:
                        raise
        raise RuntimeError("Max retries exceeded")

    async def get_repo(self, owner_repo: str) -> Optional[dict]:
        resp = await self._request("GET", f"{GITHUB_API}/repos/{owner_repo}")
        return resp.json() if resp.status_code == 200 else None

    async def list_repos(self, org: str, per_page: int = 100) -> list[dict]:
        repos = []
        page = 1
        while True:
            resp = await self._request(
                "GET", f"{GITHUB_API}/orgs/{org}/repos",
                params={"per_page": per_page, "page": page},
            )
            if resp.status_code != 200:
                break
            batch = resp.json()
            if not batch:
                break
            repos.extend(batch)
            page += 1
        return repos

    async def get_file_content(self, owner_repo: str, path: str) -> Optional[str]:
        resp = await self._request("GET", f"{GITHUB_API}/repos/{owner_repo}/contents/{path}")
        if resp.status_code != 200:
            return None
        data = resp.json()
        return base64.b64decode(data["content"]).decode()

    async def update_file(
        self, owner_repo: str, path: str, content: str, message: str, branch: str = "main",
    ) -> bool:
        # Get current SHA
        resp = await self._request("GET", f"{GITHUB_API}/repos/{owner_repo}/contents/{path}")
        sha = resp.json().get("sha") if resp.status_code == 200 else None

        payload: dict[str, Any] = {
            "message": message,
            "content": base64.b64encode(content.encode()).decode(),
            "branch": branch,
        }
        if sha:
            payload["sha"] = sha

        resp = await self._request(
            "PUT", f"{GITHUB_API}/repos/{owner_repo}/contents/{path}", json=payload,
        )
        return resp.status_code in (200, 201)
