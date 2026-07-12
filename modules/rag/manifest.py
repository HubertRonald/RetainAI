"""Manifest helpers for generated RetainAI RAG evidence documents."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from modules.rag.schemas import RagDocument


@dataclass(frozen=True)
class RagManifestEntry:
    """Single generated RAG document manifest entry."""

    document_id: str
    document_type: str
    title: str
    local_output_path: str
    s3_target_uri: str
    source_artifact: str
    tags: list[str]


@dataclass(frozen=True)
class RagDocumentManifest:
    """Manifest for a batch of generated RAG evidence documents."""

    generated_at_utc: str
    local_documents_path: str
    s3_documents_prefix: str
    document_count: int
    entries: list[RagManifestEntry]

    def to_dict(self) -> dict[str, Any]:
        """Serialize manifest to a JSON-compatible dictionary."""
        return {
            "generated_at_utc": self.generated_at_utc,
            "local_documents_path": self.local_documents_path,
            "s3_documents_prefix": self.s3_documents_prefix,
            "document_count": self.document_count,
            "entries": [asdict(entry) for entry in self.entries],
        }


def build_manifest(
    *,
    documents: list[RagDocument],
    local_documents_path: Path,
    s3_documents_prefix: str,
) -> RagDocumentManifest:
    """Build a RAG document manifest."""
    clean_s3_prefix = s3_documents_prefix.rstrip("/") + "/"
    entries = []

    for document in documents:
        local_output = local_documents_path / document.filename
        entries.append(
            RagManifestEntry(
                document_id=document.metadata.document_id,
                document_type=document.metadata.document_type,
                title=document.metadata.title,
                local_output_path=str(local_output),
                s3_target_uri=f"{clean_s3_prefix}{document.filename}",
                source_artifact=document.metadata.source_artifact,
                tags=document.metadata.tags,
            )
        )

    return RagDocumentManifest(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        local_documents_path=str(local_documents_path),
        s3_documents_prefix=clean_s3_prefix,
        document_count=len(entries),
        entries=entries,
    )


def write_manifest(manifest: RagDocumentManifest, output_path: Path) -> Path:
    """Write a RAG manifest to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(manifest.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_path
