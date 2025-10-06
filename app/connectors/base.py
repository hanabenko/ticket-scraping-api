from __future__ import annotations
from typing import Any, Iterable, List, Dict, Optional
import json
import httpx


async def fetch_json_http(url: str, timeout_s: float = 15.0) -> Any:
    async with httpx.AsyncClient(timeout=timeout_s) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()


def read_json_file(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


import httpx as _httpx_sync


def fetch_json_http_sync(url: str, timeout_s: float = 15.0):
    with _httpx_sync.Client(timeout=timeout_s, follow_redirects=True) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.json()
