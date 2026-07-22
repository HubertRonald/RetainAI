"""RAG evidence document generation for RetainAI.

This package converts model reports, explainability artifacts and responsible-use
content into structured markdown documents with metadata. It does not call
LLM providers or cloud services directly.
"""

from modules.rag.document_builder import build_rag_documents
from modules.rag.manifest import RagDocumentManifest, RagManifestEntry, write_manifest
from modules.rag.schemas import RagDocument, RagDocumentMetadata

__all__ = [
    "build_rag_documents",
    "RagDocument",
    "RagDocumentMetadata",
    "RagDocumentManifest",
    "RagManifestEntry",
    "write_manifest",
]
