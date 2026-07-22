locals {
  quota_table_name = coalesce(
    var.quota_table_name,
    "retainai-${var.environment}-ai-usage-quota",
  )
}

variable "quota_enabled" {
  description = "Whether AI quota enforcement is enabled in the Lambda backend."
  type        = bool
  default     = true
}

variable "quota_table_name" {
  description = "Optional DynamoDB quota table name. Null derives an environment-specific name."
  type        = string
  default     = null
  nullable    = true
}

variable "quota_limit" {
  description = "Maximum AI-backed requests per client and fixed window."
  type        = number
  default     = 3

  validation {
    condition     = var.quota_limit > 0
    error_message = "quota_limit must be greater than zero."
  }
}

variable "quota_window_seconds" {
  description = "Fixed quota window in seconds. The Sprint 7.6 default is 24 hours."
  type        = number
  default     = 86400

  validation {
    condition     = var.quota_window_seconds > 0
    error_message = "quota_window_seconds must be greater than zero."
  }
}

variable "ai_endpoint_prefixes" {
  description = "URL prefixes treated as AI-backed and subject to fail-closed provider and quota controls."
  type        = list(string)
  default = [
    "/advisor",
    "/api/advisor",
    "/ai",
    "/rag",
  ]
}

resource "aws_dynamodb_table" "ai_usage_quota" {
  name         = local.quota_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "quota_key"

  attribute {
    name = "quota_key"
    type = "S"
  }

  ttl {
    attribute_name = "expires_at"
    enabled        = true
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = true
  }

  tags = merge(
    var.tags,
    {
      Name      = local.quota_table_name
      component = "ai-quota"
    },
  )
}

resource "aws_iam_role_policy" "lambda_quota" {
  name = "${var.lambda_function_name}-quota"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "RetainAIQuotaTableAccess"
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
        ]
        Resource = aws_dynamodb_table.ai_usage_quota.arn
      },
    ]
  })
}

output "quota_table_name" {
  description = "DynamoDB table used for RetainAI AI usage quota."
  value       = aws_dynamodb_table.ai_usage_quota.name
}

output "quota_table_arn" {
  description = "ARN of the DynamoDB quota table."
  value       = aws_dynamodb_table.ai_usage_quota.arn
}
