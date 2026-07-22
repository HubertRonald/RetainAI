provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Application = "RetainAI"
      ManagedBy   = "Terraform"
      Purpose     = "GitHubActionsApplicationRelease"
    }
  }
}
