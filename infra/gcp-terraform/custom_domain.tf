resource "google_cloud_run_domain_mapping" "dashboard" {
  project  = var.project_id
  name     = var.dashboard_custom_domain
  location = google_cloud_run_v2_service.dashboard.location

  metadata {
    namespace = var.project_id
  }

  spec {
    route_name       = google_cloud_run_v2_service.dashboard.name
    certificate_mode = "AUTOMATIC"
  }

  depends_on = [
    google_cloud_run_v2_service.dashboard,
    google_cloud_run_v2_service_iam_member.dashboard_public_invoker,
  ]
}
