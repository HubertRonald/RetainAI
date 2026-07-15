output "artifact_registry_repository_id" {
  description = "Artifact Registry repository ID."
  value       = google_artifact_registry_repository.dashboard.repository_id
}

output "artifact_registry_repository_name" {
  description = "Artifact Registry repository resource name."
  value       = google_artifact_registry_repository.dashboard.name
}

output "dashboard_service_name" {
  description = "Cloud Run dashboard service name."
  value       = google_cloud_run_v2_service.dashboard.name
}

output "dashboard_service_uri" {
  description = "Cloud Run dashboard service URI."
  value       = google_cloud_run_v2_service.dashboard.uri
}

output "dashboard_service_account_email" {
  description = "Cloud Run dashboard service account."
  value       = google_service_account.dashboard.email
}

output "dashboard_image_uri" {
  description = "Dashboard container image URI."
  value       = var.dashboard_image_uri
}

output "dashboard_runtime_api_url" {
  description = "Server-side AWS backend URL configured in Cloud Run."
  value       = var.dashboard_api_url
  sensitive   = false
}
