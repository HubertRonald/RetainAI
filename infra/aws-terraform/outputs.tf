output "aws_account_id" {
  description = "AWS account ID used by Terraform."
  value       = data.aws_caller_identity.current.account_id
}

output "ecr_repository_name" {
  description = "ECR repository name."
  value       = aws_ecr_repository.backend.name
}

output "ecr_repository_url" {
  description = "ECR repository URL."
  value       = aws_ecr_repository.backend.repository_url
}

output "lambda_function_name" {
  description = "Lambda backend function name."
  value       = aws_lambda_function.backend.function_name
}

output "lambda_function_arn" {
  description = "Lambda backend function ARN."
  value       = aws_lambda_function.backend.arn
}

output "api_id" {
  description = "API Gateway HTTP API ID."
  value       = aws_apigatewayv2_api.backend.id
}

output "api_endpoint" {
  description = "API Gateway HTTP API endpoint."
  value       = aws_apigatewayv2_api.backend.api_endpoint
}

output "health_url" {
  description = "API Gateway health endpoint."
  value       = "${aws_apigatewayv2_api.backend.api_endpoint}/health"
}
