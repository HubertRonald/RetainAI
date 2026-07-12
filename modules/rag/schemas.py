"""Schemas for RetainAI RAG evidence documents.

The module intentionally uses dataclasses instead of Pydantic so it can be used
from local scripts, tests, Lambda containers and notebooks without additional
runtime assumptions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import re
from typing import Any


def slugify(value: str) -> str:
    """Return a filesystem-safe slug."""
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "document"


@dataclass(frozen=True)
class RagDocumentMetadata:
    """Metadata attached to a generated RAG evidence document."""

    document_id: str
    document_type: str
    title: str
    source_artifact: str
    local_output_path: str
    s3_target_prefix: str
    model_name: str | None = None
    employee_segment: str | None = None
    risk_level: str | None = None
    top_drivers: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    generated_at_utc: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        """Serialize metadata to a dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class RagDocument:
    """Generated markdown document plus metadata."""

    metadata: RagDocumentMetadata
    body: str

    @property
    def filename(self) -> str:
        """Return the recommended markdown filename."""
        return f"{slugify(self.metadata.document_id)}.md"

    def to_markdown(self) -> str:
        """Render the document as markdown with YAML-like metadata."""
        lines = [
            "---",
            f"document_id: {self.metadata.document_id}",
            f"document_type: {self.metadata.document_type}",
            f"title: {self.metadata.title}",
            f"source_artifact: {self.metadata.source_artifact}",
            f"s3_target_prefix: {self.metadata.s3_target_prefix}",
        ]

        if self.metadata.model_name:
            lines.append(f"model_name: {self.metadata.model_name}")

        if self.metadata.employee_segment:
            lines.append(f"employee_segment: {self.metadata.employee_segment}")

        if self.metadata.risk_level:
            lines.append(f"risk_level: {self.metadata.risk_level}")

        if self.metadata.top_drivers:
            lines.append("top_drivers:")
            for driver in self.metadata.top_drivers:
                lines.append(f"  - {driver}")

        if self.metadata.tags:
            lines.append("tags:")
            for tag in self.metadata.tags:
                lines.append(f"  - {tag}")

        lines.extend(
            [
                f"generated_at_utc: {self.metadata.generated_at_utc}",
                "---",
                "",
                self.body.strip(),
                "",
            ]
        )
        return "\n".join(lines)
