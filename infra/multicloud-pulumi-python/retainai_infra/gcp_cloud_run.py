"""Google Cloud Run dashboard resources for RetainAI.

Sprint 7.4 scope:
- Preview a Cloud Run v2 service skeleton for the Streamlit dashboard.
- Define runtime environment variables.
- Do not bake secrets into the container image.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pulumi
import pulumi_gcp as gcp


@dataclass(frozen=True)
class CloudRunDashboardConfig:
    """Configuration for the RetainAI dashboard Cloud Run service."""

    project_id: str
    region: str
    image_uri: str
    api_url: str
    service_name: str = "retainai-dashboard"
    allow_public: bool = True
    min_instance_count: int = 0
    max_instance_count: int = 1
    container_port: int = 8501
    cpu_limit: str = "1"
    memory_limit: str = "1Gi"
    service_account_email: str | None = None
    backend_token_secret_id: str | None = None
    environment: str = "dev"
    extra_env: dict[str, str] = field(default_factory=dict)


def _base_env(config: CloudRunDashboardConfig) -> list[gcp.cloudrunv2.ServiceTemplateContainerEnvArgs]:
    """Build non-secret environment variables for Cloud Run."""
    values = {
        "RETAINAI_ENV": config.environment,
        "RETAINAI_DASHBOARD_MODE": "api",
        "RETAINAI_API_PROVIDER": "aws-lambda",
        "RETAINAI_API_URL": config.api_url,
        "RETAINAI_AI_PROVIDER": "disabled",
        "RETAINAI_ENABLE_RAG": "false",
        "RETAINAI_VECTOR_STORE": "disabled",
        **config.extra_env,
    }

    return [
        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(name=name, value=value)
        for name, value in sorted(values.items())
    ]


def _secret_env(
    config: CloudRunDashboardConfig,
) -> list[gcp.cloudrunv2.ServiceTemplateContainerEnvArgs]:
    """Build optional secret-backed environment variables."""
    if not config.backend_token_secret_id:
        return []

    return [
        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
            name="RETAINAI_BACKEND_TOKEN",
            value_source=gcp.cloudrunv2.ServiceTemplateContainerEnvValueSourceArgs(
                secret_key_ref=gcp.cloudrunv2.ServiceTemplateContainerEnvValueSourceSecretKeyRefArgs(
                    secret=config.backend_token_secret_id,
                    version="latest",
                )
            ),
        )
    ]


def create_cloud_run_dashboard(
    config: CloudRunDashboardConfig,
) -> gcp.cloudrunv2.Service:
    """Create a Cloud Run v2 service for the RetainAI dashboard."""
    envs = _base_env(config) + _secret_env(config)

    service = gcp.cloudrunv2.Service(
        "retainai-dashboard-cloud-run",
        name=config.service_name,
        project=config.project_id,
        location=config.region,
        ingress="INGRESS_TRAFFIC_ALL",
        template=gcp.cloudrunv2.ServiceTemplateArgs(
            service_account=config.service_account_email,
            scaling=gcp.cloudrunv2.ServiceTemplateScalingArgs(
                min_instance_count=config.min_instance_count,
                max_instance_count=config.max_instance_count,
            ),
            containers=[
                gcp.cloudrunv2.ServiceTemplateContainerArgs(
                    image=config.image_uri,
                    ports=[
                        gcp.cloudrunv2.ServiceTemplateContainerPortArgs(
                            container_port=config.container_port,
                        )
                    ],
                    envs=envs,
                    resources=gcp.cloudrunv2.ServiceTemplateContainerResourcesArgs(
                        limits={
                            "cpu": config.cpu_limit,
                            "memory": config.memory_limit,
                        }
                    ),
                )
            ],
        ),
    )

    if config.allow_public:
        gcp.cloudrunv2.ServiceIamMember(
            "retainai-dashboard-public-invoker",
            project=config.project_id,
            location=config.region,
            name=service.name,
            role="roles/run.invoker",
            member="allUsers",
        )

    pulumi.export("dashboard_cloud_run_service", service.name)
    pulumi.export("dashboard_cloud_run_uri", service.uri)

    return service
