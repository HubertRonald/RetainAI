data "google_project" "current" {
  project_id = var.project_id
}

resource "google_service_account" "github_release" {
  project      = var.project_id
  account_id   = var.deployment_service_account_id
  display_name = "RetainAI GitHub application release"
  description  = "Least-privilege identity for manual dashboard image releases."

  deletion_policy = "PREVENT"
}

resource "google_iam_workload_identity_pool" "github" {
  project                   = var.project_id
  workload_identity_pool_id = var.workload_identity_pool_id
  display_name              = "RetainAI GitHub Actions"
  description               = "Federated identities for the RetainAI repository."

  deletion_policy = "PREVENT"
}

resource "google_iam_workload_identity_pool_provider" "github" {
  project                            = var.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = var.workload_identity_provider_id
  display_name                       = "RetainAI main branch"
  description                        = "Accepts GitHub OIDC tokens only from RetainAI main."

  attribute_mapping = {
    "google.subject"             = "assertion.sub"
    "attribute.actor"            = "assertion.actor"
    "attribute.repository"       = "assertion.repository"
    "attribute.repository_owner" = "assertion.repository_owner"
    "attribute.ref"              = "assertion.ref"
  }

  attribute_condition = join(
    " && ",
    [
      "assertion.repository == '${var.github_repository}'",
      "assertion.ref == '${var.github_branch_ref}'",
    ],
  )

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }

  deletion_policy = "PREVENT"
}

resource "google_service_account_iam_member" "github_workload_identity_user" {
  service_account_id = google_service_account.github_release.name
  role               = "roles/iam.workloadIdentityUser"

  member = "principalSet://iam.googleapis.com/projects/${data.google_project.current.number}/locations/global/workloadIdentityPools/${google_iam_workload_identity_pool.github.workload_identity_pool_id}/attribute.repository/${var.github_repository}"
}

resource "google_artifact_registry_repository_iam_member" "artifact_registry_writer" {
  project    = var.project_id
  location   = var.region
  repository = var.artifact_repository_id
  role       = "roles/artifactregistry.writer"

  member = "serviceAccount:${google_service_account.github_release.email}"
}

resource "google_cloud_run_v2_service_iam_member" "cloud_run_developer" {
  project  = var.project_id
  location = var.region
  name     = var.dashboard_service_name
  role     = "roles/run.developer"

  member = "serviceAccount:${google_service_account.github_release.email}"
}

resource "google_service_account_iam_member" "runtime_service_account_user" {
  service_account_id = "projects/${var.project_id}/serviceAccounts/${var.cloud_run_runtime_service_account_email}"
  role               = "roles/iam.serviceAccountUser"

  member = "serviceAccount:${google_service_account.github_release.email}"
}
