from __future__ import annotations

import requests


class APIConnector:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def get(self, path: str) -> dict:
        r = requests.get(f"{self.base_url}{path}", timeout=10)
        r.raise_for_status()
        return r.json()

    def post(self, path: str, payload: dict) -> dict:
        r = requests.post(f"{self.base_url}{path}", json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
