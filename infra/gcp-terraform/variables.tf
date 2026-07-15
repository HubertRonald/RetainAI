variable "project_id" {
  description = "Existing GCP project ID with billing enabled."
  type        = string
}

variable "region" {
  description = "GCP region for Artifact Registry and Cloud Run. RetainAI uses us-east4 to align with AWS us-east-1."
  type        = string
  default     = "us-east4"
}

variable "environment" {
  description = "Logical environment name."
  type        = string
  default     = "dev"
}

variable "artifact_repository_id" {
  description = "Artifact Registry Docker repository ID for the RetainAI dashboard image."
  type        = string
  default     = "retainai-dashboard"
}

variable "dashboard_service_name" {
  description = "Cloud Run service name for the RetainAI dashboard."
  type        = string
  default     = "retainai-dashboard"
}

variable "dashboard_image_uri" {
  description = "Full dashboard image URI in Artifact Registry."
  type        = string
}

variable "dashboard_api_url" {
  description = "AWS backend URL consumed server-side by the Cloud Run dashboard."
  type        = string
}

variable "dashboard_allow_public" {
  description = "Whether the Cloud Run dashboard should be publicly invokable."
  type        = bool
  default     = true
}

variable "dashboard_min_instances" {
  description = "Minimum Cloud Run instances."
  type        = number
  default     = 0
}

variable "dashboard_max_instances" {
  description = "Maximum Cloud Run instances for low-cost portfolio traffic."
  type        = number
  default     = 1
}

variable "dashboard_container_port" {
  description = "Streamlit container port."
  type        = number
  default     = 8501
}

variable "dashboard_cpu_limit" {
  description = "Cloud Run dashboard CPU limit."
  type        = string
  default     = "1"
}

variable "dashboard_memory_limit" {
  description = "Cloud Run dashboard memory limit."
  type        = string
  default     = "1Gi"
}

variable "dashboard_backend_token_secret_id" {
  description = "Optional Secret Manager secret ID for backend token. Leave null for Sprint 7.4 skeleton."
  type        = string
  default     = null
  nullable    = true
}

variable "labels" {
  description = "Common labels for RetainAI GCP resources."
  type        = map(string)

  default = {
    app      = "retainai"
    env      = "dev"
    platform = "decision-intelligence"
    managed  = "terraform"
  }
}
