variable "aws_region" {
  description = "AWS region for the RetainAI backend. RetainAI uses us-east-1 to align with GCP us-east4."
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Logical deployment environment."
  type        = string
  default     = "dev"
}

variable "ecr_repository_name" {
  description = "ECR repository for the RetainAI API Lambda container image."
  type        = string
  default     = "retainai-api-lambda"
}

variable "lambda_function_name" {
  description = "AWS Lambda function name for the RetainAI backend."
  type        = string
  default     = "retainai-api-backend"
}

variable "lambda_image_uri" {
  description = "Full ECR image URI for the Lambda container."
  type        = string
}

variable "lambda_memory_size" {
  description = "Lambda memory size in MB."
  type        = number
  default     = 1024
}

variable "lambda_timeout_seconds" {
  description = "Lambda timeout in seconds."
  type        = number
  default     = 60
}

variable "backend_auth_enabled" {
  description = "Whether the Lambda handler should require a backend token for non-health endpoints."
  type        = bool
  default     = true
}

variable "backend_token" {
  description = "Optional backend token for protected endpoints. For production, prefer Secrets Manager or CI/CD secrets."
  type        = string
  default     = null
  sensitive   = true
  nullable    = true
}

variable "api_name" {
  description = "API Gateway HTTP API name."
  type        = string
  default     = "retainai-api-http"
}

variable "cors_allow_origins" {
  description = "Allowed CORS origins. Use Cloud Run URL after deployment."
  type        = list(string)
  default     = ["*"]
}

variable "tags" {
  description = "Common AWS tags."
  type        = map(string)

  default = {
    app      = "retainai"
    env      = "dev"
    platform = "decision-intelligence"
    managed  = "terraform"
  }
}
