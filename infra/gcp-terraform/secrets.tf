resource "google_secret_manager_secret" "dashboard_backend_token" {
  count = var.dashboard_backend_token_secret_id == null ? 0 : 1

  project   = var.project_id
  secret_id = var.dashboard_backend_token_secret_id
  labels    = var.labels

  replication {
    auto {}
  }

  depends_on = [
    google_project_service.services["secretmanager.googleapis.com"],
  ]
}

resource "google_secret_manager_secret_iam_member" "dashboard_backend_token_accessor" {
  count = var.dashboard_backend_token_secret_id == null ? 0 : 1

  project   = var.project_id
  secret_id = google_secret_manager_secret.dashboard_backend_token[0].secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.dashboard.email}"
}

output "dashboard_backend_token_secret_id" {
  description = "Secret Manager secret ID used by the Cloud Run dashboard."
  value       = try(google_secret_manager_secret.dashboard_backend_token[0].secret_id, null)
}

output "dashboard_backend_token_secret_name" {
  description = "Secret Manager resource name used by the Cloud Run dashboard."
  value       = try(google_secret_manager_secret.dashboard_backend_token[0].name, null)
}
