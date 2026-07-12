"""Vector-store interfaces for RetainAI RAG retrieval."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class VectorDocument:
    """Document stored in a vector index."""

    document_id: str
    title: str
    text: str
    source_path: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VectorSearchResult:
    """Single vector search result."""

    document_id: str
    title: str
    text: str
    score: float
    source_path: str
    metadata: dict[str, Any] = field(default_factory=dict)


class VectorStore(ABC):
    """Abstract vector-store contract."""

    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> list[VectorSearchResult]:
        """Retrieve top-k documents for a query."""


def normalize_s3_prefix(prefix: str) -> str:
    """Return a normalized S3 prefix ending in '/'."""
    return prefix.rstrip("/") + "/"
