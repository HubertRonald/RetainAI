output "github_actions_release_role_arn" {
  description = "Set this value as AWS_ROLE_TO_ASSUME in each GitHub environment."
  value       = aws_iam_role.application_release.arn
}

output "github_oidc_provider_arn" {
  description = "GitHub OIDC provider used by the release role."
  value       = local.github_oidc_provider_arn
}
