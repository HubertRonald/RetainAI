output "workload_identity_provider" {
  description = "Set this as GCP_WORKLOAD_IDENTITY_PROVIDER in the GitHub environment."
  value       = google_iam_workload_identity_pool_provider.github.name
}

output "deployment_service_account_email" {
  description = "Set this as GCP_DEPLOY_SERVICE_ACCOUNT in the GitHub environment."
  value       = google_service_account.github_release.email
}

output "artifact_registry_repository" {
  description = "Artifact Registry repository receiving dashboard images."
  value       = var.artifact_repository_id
}

output "cloud_run_service" {
  description = "Cloud Run service updated by GitHub Actions."
  value       = var.dashboard_service_name
}
