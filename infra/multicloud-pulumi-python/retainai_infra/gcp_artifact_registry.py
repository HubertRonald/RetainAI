"""Google Artifact Registry resources for RetainAI.

Sprint 7.4 scope:
- Create a Docker Artifact Registry repository for the Cloud Run dashboard image.
- Keep image build/push outside Pulumi for now.
"""

from __future__ import annotations

from dataclasses import dataclass

import pulumi
import pulumi_gcp as gcp


@dataclass(frozen=True)
class ArtifactRegistryConfig:
    """Configuration for a RetainAI Artifact Registry repository."""

    project_id: str
    region: str
    repository_id: str = "retainai-dashboard"
    description: str = "RetainAI dashboard container images"


def create_dashboard_artifact_registry(
    config: ArtifactRegistryConfig,
) -> gcp.artifactregistry.Repository:
    """Create the Artifact Registry Docker repository for dashboard images."""
    repository = gcp.artifactregistry.Repository(
        "retainai-dashboard-artifact-registry",
        project=config.project_id,
        location=config.region,
        repository_id=config.repository_id,
        description=config.description,
        format="DOCKER",
    )

    pulumi.export("dashboard_artifact_registry_repository", repository.name)
    pulumi.export("dashboard_artifact_registry_location", repository.location)

    return repository
