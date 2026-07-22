output "workload_identity_provider" {
  description = "Set this value as GCP_WORKLOAD_IDENTITY_PROVIDER in each GitHub environment."
  value       = google_iam_workload_identity_pool_provider.github.name
}

output "deployment_service_account_email" {
  description = "Set this value as GCP_DEPLOY_SERVICE_ACCOUNT in each GitHub environment."
  value       = google_service_account.github_release.email
}
