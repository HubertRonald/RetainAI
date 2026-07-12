"""Manifest helpers for RetainAI local data lake artifacts.

The manifest intentionally performs local filesystem inspection only.
S3 upload/sync remains a separate, explicit operator action.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Iterable

from modules.data_lake.zone_mapping import ZoneMapping, build_default_zone_mappings


@dataclass(frozen=True)
class ManifestEntry:
    """Single local artifact entry mapped to a target S3 URI."""

    mapping_name: str
    local_path: str
    s3_uri: str
    size_bytes: int
    sha256: str


@dataclass(frozen=True)
class DataLakeManifest:
    """Data lake manifest for local-to-S3 seed review."""

    generated_at_utc: str
    environment: str
    bucket: str
    entries: list[ManifestEntry]

    def to_dict(self) -> dict[str, object]:
        """Serialize manifest to a JSON-compatible dictionary."""
        return {
            "generated_at_utc": self.generated_at_utc,
            "environment": self.environment,
            "bucket": self.bucket,
            "entries": [asdict(entry) for entry in self.entries],
        }

    def write_json(self, output_path: Path) -> Path:
        """Write manifest as pretty JSON."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return output_path


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _iter_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    return (path for path in root.rglob("*") if path.is_file())


def build_manifest(
    *,
    bucket: str,
    environment: str = "dev",
    project_root: Path | str = ".",
    mappings: list[ZoneMapping] | None = None,
) -> DataLakeManifest:
    """Build a manifest from local files and default S3 mapping contracts."""
    root = Path(project_root)
    selected_mappings = mappings or build_default_zone_mappings()
    entries: list[ManifestEntry] = []

    for mapping in selected_mappings:
        local_root = root / mapping.local_path
        for path in _iter_files(local_root):
            relative_to_mapping = path.relative_to(local_root)
            s3_uri = f"{mapping.s3_uri(bucket)}{relative_to_mapping.as_posix()}"

            entries.append(
                ManifestEntry(
                    mapping_name=mapping.name,
                    local_path=str(path.relative_to(root)),
                    s3_uri=s3_uri,
                    size_bytes=path.stat().st_size,
                    sha256=_sha256_file(path),
                )
            )

    return DataLakeManifest(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        environment=environment,
        bucket=bucket,
        entries=entries,
    )
