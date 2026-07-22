variable "project_id" {
  description = "Google Cloud project containing RetainAI."
  type        = string
  default     = "coplayground"
}

variable "region" {
  description = "Cloud Run and Artifact Registry region."
  type        = string
  default     = "us-east4"
}

variable "github_repository" {
  description = "GitHub owner and repository."
  type        = string
  default     = "HubertRonald/RetainAI"
}

variable "workload_identity_pool_id" {
  description = "Workload Identity Pool ID."
  type        = string
  default     = "retainai-github"
}

variable "workload_identity_provider_id" {
  description = "Workload Identity Provider ID."
  type        = string
  default     = "retainai-main"
}

variable "deployment_service_account_id" {
  description = "Service account ID used by GitHub Actions."
  type        = string
  default     = "retainai-gh-release"
}

variable "cloud_run_runtime_service_account_email" {
  description = "Existing Cloud Run runtime service-account email that the deployment identity may act as."
  type        = string
}
