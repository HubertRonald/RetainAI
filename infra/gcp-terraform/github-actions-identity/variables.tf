variable "project_id" {
  description = "Google Cloud project containing the RetainAI runtime."
  type        = string
  default     = "coplayground"

  validation {
    condition     = length(trimspace(var.project_id)) > 0
    error_message = "project_id cannot be empty."
  }
}

variable "region" {
  description = "Region containing Artifact Registry and Cloud Run."
  type        = string
  default     = "us-east4"

  validation {
    condition     = length(trimspace(var.region)) > 0
    error_message = "region cannot be empty."
  }
}

variable "github_repository" {
  description = "GitHub repository allowed to use Workload Identity Federation."
  type        = string
  default     = "HubertRonald/RetainAI"

  validation {
    condition     = can(regex("^[^/]+/[^/]+$", var.github_repository))
    error_message = "github_repository must use the OWNER/REPOSITORY format."
  }
}

variable "github_branch_ref" {
  description = "Exact Git ref allowed to authenticate."
  type        = string
  default     = "refs/heads/main"

  validation {
    condition     = startswith(var.github_branch_ref, "refs/heads/")
    error_message = "github_branch_ref must be a branch ref such as refs/heads/main."
  }
}

variable "workload_identity_pool_id" {
  description = "ID of the Workload Identity Pool used by GitHub Actions."
  type        = string
  default     = "retainai-github"
}

variable "workload_identity_provider_id" {
  description = "ID of the GitHub Workload Identity Provider."
  type        = string
  default     = "retainai-main"
}

variable "deployment_service_account_id" {
  description = "Account ID of the service account impersonated by GitHub Actions."
  type        = string
  default     = "retainai-gh-release"
}

variable "artifact_repository_id" {
  description = "Existing Artifact Registry repository receiving dashboard images."
  type        = string
  default     = "retainai-dashboard"

  validation {
    condition     = length(trimspace(var.artifact_repository_id)) > 0
    error_message = "artifact_repository_id cannot be empty."
  }
}

variable "dashboard_service_name" {
  description = "Existing Cloud Run service updated by the release workflow."
  type        = string
  default     = "retainai-dashboard"

  validation {
    condition     = length(trimspace(var.dashboard_service_name)) > 0
    error_message = "dashboard_service_name cannot be empty."
  }
}

variable "cloud_run_runtime_service_account_email" {
  description = "Existing service account used by the Cloud Run dashboard revision."
  type        = string

  validation {
    condition = can(
      regex(
        "^[a-z][a-z0-9-]{4,28}[a-z0-9]@[a-z][a-z0-9-]{4,28}[a-z0-9][.]iam[.]gserviceaccount[.]com$",
        var.cloud_run_runtime_service_account_email,
      )
    )
    error_message = "cloud_run_runtime_service_account_email must be a valid Google service-account email."
  }
}
