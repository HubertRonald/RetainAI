"""Local-to-S3 data lake zone mapping for RetainAI."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class DataLakeZone(str, Enum):
    """Supported RetainAI data lake zones.

    Implemented as str + Enum for Python 3.10 compatibility.
    """

    RAW = "raw"
    STAGING = "staging"
    ANALYTICS = "analytics"
    FEATURES = "features"
    MODEL_ARTIFACTS = "model-artifacts"
    MONITORING = "monitoring"
    DASHBOARD_EXPORTS = "dashboard-exports"


@dataclass(frozen=True)
class ZoneMapping:
    """Mapping between a local project path and an S3 data lake prefix."""

    name: str
    local_path: Path
    zone: DataLakeZone
    s3_prefix: str
    description: str

    def s3_uri(self, bucket: str) -> str:
        """Return a normalized S3 URI for this mapping."""
        clean_bucket = bucket.replace("s3://", "").strip("/")
        clean_prefix = self.s3_prefix.strip("/")
        return f"s3://{clean_bucket}/{clean_prefix}/"


def build_default_zone_mappings() -> list[ZoneMapping]:
    """Build the default RetainAI local-to-S3 data lake mappings."""
    return [
        ZoneMapping(
            name="raw",
            local_path=Path("data/raw"),
            zone=DataLakeZone.RAW,
            s3_prefix="raw",
            description="Original source data, unchanged.",
        ),
        ZoneMapping(
            name="prediction_input",
            local_path=Path("data/prediction_input"),
            zone=DataLakeZone.RAW,
            s3_prefix="raw/prediction-input",
            description="Files uploaded through dashboard or CLI for scoring.",
        ),
        ZoneMapping(
            name="processed",
            local_path=Path("data/processed"),
            zone=DataLakeZone.ANALYTICS,
            s3_prefix="analytics/processed",
            description="Cleaned and typed analytics-ready dataset.",
        ),
        ZoneMapping(
            name="train",
            local_path=Path("data/train"),
            zone=DataLakeZone.FEATURES,
            s3_prefix="features/train",
            description="Training split and feature matrix.",
        ),
        ZoneMapping(
            name="validation",
            local_path=Path("data/validation"),
            zone=DataLakeZone.FEATURES,
            s3_prefix="features/validation",
            description="Validation split for model selection and dashboard checks.",
        ),
        ZoneMapping(
            name="test",
            local_path=Path("data/test"),
            zone=DataLakeZone.FEATURES,
            s3_prefix="features/test",
            description="Final holdout split and demo scoring data.",
        ),
        ZoneMapping(
            name="models",
            local_path=Path("artifacts/models"),
            zone=DataLakeZone.MODEL_ARTIFACTS,
            s3_prefix="model-artifacts/models",
            description="Serialized pipelines, metrics and model registry outputs.",
        ),
        ZoneMapping(
            name="explanations",
            local_path=Path("artifacts/explanations"),
            zone=DataLakeZone.MODEL_ARTIFACTS,
            s3_prefix="model-artifacts/explanations",
            description="SHAP and local/global explanation artifacts.",
        ),
        ZoneMapping(
            name="reports",
            local_path=Path("artifacts/reports"),
            zone=DataLakeZone.MODEL_ARTIFACTS,
            s3_prefix="model-artifacts/reports",
            description="Model, survival and explainability reports.",
        ),
        ZoneMapping(
            name="figures",
            local_path=Path("artifacts/figures"),
            zone=DataLakeZone.MODEL_ARTIFACTS,
            s3_prefix="model-artifacts/figures",
            description="Generated model and dashboard figures.",
        ),
        ZoneMapping(
            name="rag",
            local_path=Path("artifacts/rag"),
            zone=DataLakeZone.MODEL_ARTIFACTS,
            s3_prefix="model-artifacts/rag",
            description="RAG documents, manifests and vector indexes.",
        ),
        ZoneMapping(
            name="dashboard",
            local_path=Path("artifacts/dashboard"),
            zone=DataLakeZone.DASHBOARD_EXPORTS,
            s3_prefix="dashboard-exports",
            description="Dashboard-generated downloadable outputs.",
        ),
        ZoneMapping(
            name="monitoring",
            local_path=Path("artifacts/monitoring"),
            zone=DataLakeZone.MONITORING,
            s3_prefix="monitoring",
            description="Feature drift, prediction drift and scoring logs.",
        ),
    ]


def get_zone_mapping(name: str) -> ZoneMapping:
    """Return a mapping by name.

    Raises:
        KeyError: if the mapping does not exist.
    """
    mappings = {mapping.name: mapping for mapping in build_default_zone_mappings()}
    try:
        return mappings[name]
    except KeyError as exc:
        available = ", ".join(sorted(mappings))
        raise KeyError(
            f"Unknown data lake mapping '{name}'. Available: {available}"
        ) from exc
