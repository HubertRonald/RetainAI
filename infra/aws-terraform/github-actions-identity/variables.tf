variable "aws_region" {
  description = "AWS region containing the RetainAI backend."
  type        = string
  default     = "us-east-1"
}

variable "github_repository" {
  description = "GitHub owner and repository."
  type        = string
  default     = "HubertRonald/RetainAI"
}

variable "github_environments" {
  description = "GitHub environments allowed to assume the release role."
  type        = set(string)
  default     = ["dev", "prod"]
}

variable "create_github_oidc_provider" {
  description = "Create the account-level GitHub OIDC provider when it does not already exist."
  type        = bool
  default     = false
}

variable "role_name" {
  description = "IAM role assumed by the manual application-release workflow."
  type        = string
  default     = "retainai-github-actions-application-release"
}

variable "ecr_repository_name" {
  description = "Existing ECR repository used by the Lambda backend."
  type        = string
}

variable "lambda_function_name" {
  description = "Existing Lambda function updated by immutable image URI."
  type        = string
}
