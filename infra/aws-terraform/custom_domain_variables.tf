variable "api_custom_domain" {
  description = "Branded Regional API Gateway domain for the RetainAI backend."
  type        = string
  default     = "api.retainai.hubertronald.dev"

  validation {
    condition     = var.api_custom_domain == "api.retainai.hubertronald.dev"
    error_message = "Sprint 7.6.2 requires api.retainai.hubertronald.dev."
  }
}

variable "dashboard_allowed_origin" {
  description = "Public dashboard origin allowed by API Gateway CORS."
  type        = string
  default     = "https://retainai.hubertronald.dev"

  validation {
    condition     = startswith(var.dashboard_allowed_origin, "https://")
    error_message = "dashboard_allowed_origin must use HTTPS."
  }
}
