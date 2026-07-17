locals {
  lambda_environment = merge(
    {
      RETAINAI_ENV                  = var.environment
      RETAINAI_RUNTIME              = "aws-lambda"
      RETAINAI_BACKEND_AUTH_ENABLED = tostring(var.backend_auth_enabled)
      RETAINAI_AI_PROVIDER          = "disabled"
      RETAINAI_ENABLE_RAG           = "false"
      RETAINAI_VECTOR_STORE         = "disabled"
      RETAINAI_LOG_LEVEL            = "INFO"
      RETAINAI_QUOTA_ENABLED        = tostring(var.quota_enabled)
      RETAINAI_QUOTA_BACKEND        = var.quota_enabled ? "dynamodb" : "disabled"
      RETAINAI_QUOTA_TABLE          = local.quota_table_name
      RETAINAI_QUOTA_LIMIT          = tostring(var.quota_limit)
      RETAINAI_QUOTA_WINDOW_SECONDS = tostring(var.quota_window_seconds)
      RETAINAI_AI_ENDPOINT_PREFIXES = join(",", var.ai_endpoint_prefixes)
    },
    var.backend_token == null ? {} : {
      RETAINAI_BACKEND_TOKEN = var.backend_token
    }
  )
}

data "aws_caller_identity" "current" {}

resource "aws_ecr_repository" "backend" {
  name                 = var.ecr_repository_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }
}

resource "aws_ecr_lifecycle_policy" "backend" {
  repository = aws_ecr_repository.backend.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 backend images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 14
}

resource "aws_iam_role" "lambda" {
  name = "${var.lambda_function_name}-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "backend" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda.arn

  package_type = "Image"
  image_uri    = var.lambda_image_uri

  image_config {
    command           = ["apps.api.lambda_handler.handler"]
    working_directory = "/var/task"
  }

  memory_size = var.lambda_memory_size
  timeout     = var.lambda_timeout_seconds

  architectures = ["x86_64"]

  environment {
    variables = local.lambda_environment
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda,
    aws_iam_role_policy_attachment.lambda_basic_execution,
    aws_iam_role_policy.lambda_quota,
  ]
}

resource "aws_apigatewayv2_api" "backend" {
  name          = var.api_name
  protocol_type = "HTTP"

  cors_configuration {
    allow_headers = [
      "authorization",
      "content-type",
      "x-retainai-backend-token",
    ]
    allow_methods = [
      "GET",
      "POST",
      "OPTIONS",
    ]
    allow_origins = var.cors_allow_origins
    max_age       = 300
  }
}

resource "aws_apigatewayv2_integration" "lambda_proxy" {
  api_id                 = aws_apigatewayv2_api.backend.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.backend.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "default" {
  api_id    = aws_apigatewayv2_api.backend.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_proxy.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.backend.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowExecutionFromHttpApi"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.backend.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}
