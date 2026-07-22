"""Build a local FAISS + S3-compatible vector index from RAG documents.

No cloud calls are made.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from modules.rag.faiss_store import (
    DEFAULT_EMBEDDING_DIMENSION,
    DEFAULT_EMBEDDING_MODEL,
    deterministic_embedding,
)


@dataclass(frozen=True)
class BuildResult:
    """Vector index build result."""

    index_backend: str
    document_count: int
    index_path: str
    documents_path: str
    metadata_path: str
    manifest_path: str
    s3_prefix: str
    embedding_dimension: int
    embedding_model: str
    generated_at_utc: str


def _extract_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    raw_meta = parts[1]
    body = parts[2].strip()
    metadata: dict[str, Any] = {}
    current_list_key: str | None = None

    for line in raw_meta.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- ") and current_list_key:
            metadata.setdefault(current_list_key, []).append(stripped[2:].strip())
            continue
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                metadata[key] = value
                current_list_key = None
            else:
                metadata[key] = []
                current_list_key = key

    return metadata, body


def _document_payload(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    metadata, body = _extract_front_matter(text)
    return {
        "document_id": str(metadata.get("document_id") or path.stem),
        "title": str(metadata.get("title") or path.stem.replace("-", " ").title()),
        "source_path": str(path),
        "text": body or text,
        "metadata": metadata,
    }


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file_obj:
        for row in rows:
            file_obj.write(json.dumps(row, sort_keys=True) + "\n")
    return path


def _try_write_faiss(index_path: Path, vectors: list[list[float]]) -> bool:
    if not vectors:
        return False
    try:
        import faiss  # type: ignore
        import numpy as np  # type: ignore
    except Exception:
        return False

    array = np.array(vectors, dtype="float32")
    index = faiss.IndexFlatIP(array.shape[1])
    index.add(array)
    faiss.write_index(index, str(index_path / "index.faiss"))
    return True


def build_index(
    *,
    documents_path: Path,
    index_path: Path,
    s3_prefix: str,
    embedding_dimension: int = DEFAULT_EMBEDDING_DIMENSION,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
) -> BuildResult:
    """Build a local vector index from markdown RAG documents."""
    index_path.mkdir(parents=True, exist_ok=True)
    document_files = sorted(documents_path.glob("*.md"))

    if not document_files:
        raise FileNotFoundError(
            f"No RAG markdown documents found under {documents_path}. "
            "Run Sprint 7.2 document generation first."
        )

    documents = [_document_payload(path) for path in document_files]
    vectors = [
        deterministic_embedding(f"{document['title']}\n\n{document['text']}", embedding_dimension)
        for document in documents
    ]

    documents_jsonl_path = index_path / "documents.jsonl"
    metadata_path = index_path / "metadata.json"
    manifest_path = index_path / "manifest.json"

    _write_jsonl(documents_jsonl_path, documents)
    _write_json(index_path / "index.json", {"vectors": vectors})

    wrote_faiss = _try_write_faiss(index_path, vectors)
    backend = "faiss" if wrote_faiss else "numpy_fallback"

    metadata = {
        "index_backend": backend,
        "document_count": len(documents),
        "embedding_dimension": embedding_dimension,
        "embedding_model": embedding_model,
        "documents_path": str(documents_jsonl_path),
        "s3_prefix": s3_prefix.rstrip("/") + "/",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    _write_json(metadata_path, metadata)

    result = BuildResult(
        index_backend=backend,
        document_count=len(documents),
        index_path=str(index_path),
        documents_path=str(documents_jsonl_path),
        metadata_path=str(metadata_path),
        manifest_path=str(manifest_path),
        s3_prefix=s3_prefix.rstrip("/") + "/",
        embedding_dimension=embedding_dimension,
        embedding_model=embedding_model,
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
    )

    manifest = {
        **asdict(result),
        "files": {
            "index_faiss": str(index_path / "index.faiss") if wrote_faiss else None,
            "index_json": str(index_path / "index.json"),
            "documents_jsonl": str(documents_jsonl_path),
            "metadata_json": str(metadata_path),
            "manifest_json": str(manifest_path),
        },
        "s3_upload_plan": {
            "local_path": str(index_path),
            "s3_prefix": s3_prefix.rstrip("/") + "/",
            "dry_run_command": f"aws s3 sync {index_path}/ {s3_prefix.rstrip('/')}/ --delete --dryrun",
            "sync_command": f"aws s3 sync {index_path}/ {s3_prefix.rstrip('/')}/ --delete",
        },
    }
    _write_json(manifest_path, manifest)

    return result


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build RetainAI FAISS/S3 vector index.")
    parser.add_argument("--documents-path", default="artifacts/rag/documents")
    parser.add_argument("--index-path", default="artifacts/rag/vector-index/faiss")
    parser.add_argument("--s3-prefix", default="s3://retainai-dev-data/model-artifacts/rag/vector-index/faiss/")
    parser.add_argument("--embedding-dimension", type=int, default=DEFAULT_EMBEDDING_DIMENSION)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    result = build_index(
        documents_path=Path(args.documents_path),
        index_path=Path(args.index_path),
        s3_prefix=args.s3_prefix,
        embedding_dimension=args.embedding_dimension,
    )
    print("Built RetainAI vector index.")
    print(f"Backend: {result.index_backend}")
    print(f"Documents: {result.document_count}")
    print(f"Index path: {result.index_path}")
    print(f"Manifest path: {result.manifest_path}")
    print(f"S3 prefix: {result.s3_prefix}")


if __name__ == "__main__":
    main()
