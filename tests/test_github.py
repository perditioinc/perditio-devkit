"""Tests for perditio.github module — all external calls mocked."""

import base64

import httpx
import respx

from perditio.github import GitHubClient


@respx.mock
async def test_get_repo():
    respx.get("https://api.github.com/repos/perditioinc/test").mock(
        return_value=httpx.Response(200, json={"name": "test", "full_name": "perditioinc/test"})
    )
    client = GitHubClient(token="fake-token")
    result = await client.get_repo("perditioinc/test")
    assert result["name"] == "test"


@respx.mock
async def test_get_repo_not_found():
    respx.get("https://api.github.com/repos/perditioinc/missing").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )
    client = GitHubClient(token="fake-token")
    result = await client.get_repo("perditioinc/missing")
    assert result is None


@respx.mock
async def test_get_file_content():
    encoded = base64.b64encode(b"hello world").decode()
    respx.get("https://api.github.com/repos/perditioinc/test/contents/README.md").mock(
        return_value=httpx.Response(200, json={"content": encoded})
    )
    client = GitHubClient(token="fake-token")
    result = await client.get_file_content("perditioinc/test", "README.md")
    assert result == "hello world"


@respx.mock
async def test_update_file():
    respx.get("https://api.github.com/repos/perditioinc/test/contents/BUILD").mock(
        return_value=httpx.Response(200, json={"sha": "abc123"})
    )
    respx.put("https://api.github.com/repos/perditioinc/test/contents/BUILD").mock(
        return_value=httpx.Response(200, json={"content": {"sha": "def456"}})
    )
    client = GitHubClient(token="fake-token")
    result = await client.update_file("perditioinc/test", "BUILD", "1", "build 1")
    assert result is True
