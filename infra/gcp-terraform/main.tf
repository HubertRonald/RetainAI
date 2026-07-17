locals {
  required_services = [
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "serviceusage.googleapis.com",
    "secretmanager.googleapis.com",
    "logging.googleapis.com",
  ]

  dashboard_env = {
    RETAINAI_ENV            = var.environment
    RETAINAI_DASHBOARD_MODE = "api"
    RETAINAI_API_PROVIDER   = "aws-lambda"
    RETAINAI_API_URL        = var.dashboard_api_url
    RETAINAI_AI_PROVIDER    = "disabled"
    RETAINAI_ENABLE_RAG     = "false"
    RETAINAI_VECTOR_STORE   = "disabled"
    RETAINAI_LOG_LEVEL      = "INFO"
  }
}

resource "google_project_service" "services" {
  for_each = toset(local.required_services)

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "dashboard" {
  project       = var.project_id
  location      = var.region
  repository_id = var.artifact_repository_id
  description   = "RetainAI dashboard container images"
  format        = "DOCKER"
  labels        = var.labels

  depends_on = [
    google_project_service.services,
  ]
}

resource "google_service_account" "dashboard" {
  project      = var.project_id
  account_id   = "sa-retainai-dashboard"
  display_name = "RetainAI dashboard Cloud Run service account"
  description  = "Service account used by the RetainAI Cloud Run dashboard."

  depends_on = [
    google_project_service.services,
  ]
}

resource "google_cloud_run_v2_service" "dashboard" {
  provider = google-beta

  name                = var.dashboard_service_name
  project             = var.project_id
  location            = var.region
  ingress             = "INGRESS_TRAFFIC_ALL"
  deletion_protection = false

  template {
    service_account                  = google_service_account.dashboard.email
    max_instance_request_concurrency = 10
    timeout                          = "300s"

    scaling {
      min_instance_count = var.dashboard_min_instances
      max_instance_count = var.dashboard_max_instances
    }

    containers {
      image = var.dashboard_image_uri

      ports {
        container_port = var.dashboard_container_port
      }

      resources {
        limits = {
          cpu    = var.dashboard_cpu_limit
          memory = var.dashboard_memory_limit
        }

        startup_cpu_boost = true
      }

      dynamic "env" {
        for_each = local.dashboard_env

        content {
          name  = env.key
          value = env.value
        }
      }

      dynamic "env" {
        for_each = var.dashboard_backend_token_secret_id == null ? [] : [var.dashboard_backend_token_secret_id]

        content {
          name = "RETAINAI_BACKEND_TOKEN"

          value_source {
            secret_key_ref {
              secret  = env.value
              version = "latest"
            }
          }
        }
      }
    }
  }

  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
    ]
  }

  depends_on = [
    google_project_service.services,
    google_artifact_registry_repository.dashboard,
    google_secret_manager_secret_iam_member.dashboard_backend_token_accessor,
  ]
}

resource "google_cloud_run_v2_service_iam_member" "dashboard_public_invoker" {
  count = var.dashboard_allow_public ? 1 : 0

  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.dashboard.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
