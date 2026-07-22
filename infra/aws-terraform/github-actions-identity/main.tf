data "aws_caller_identity" "current" {}

resource "aws_iam_openid_connect_provider" "github" {
  count = var.create_github_oidc_provider ? 1 : 0

  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com",
  ]
}

locals {
  github_oidc_provider_arn = var.create_github_oidc_provider ? (
    aws_iam_openid_connect_provider.github[0].arn
    ) : (
    "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"
  )

  github_environment_subjects = [
    for environment in var.github_environments :
    "repo:${var.github_repository}:environment:${environment}"
  ]

  ecr_repository_arn  = "arn:aws:ecr:${var.aws_region}:${data.aws_caller_identity.current.account_id}:repository/${var.ecr_repository_name}"
  lambda_function_arn = "arn:aws:lambda:${var.aws_region}:${data.aws_caller_identity.current.account_id}:function:${var.lambda_function_name}"
}

data "aws_iam_policy_document" "github_trust" {
  statement {
    sid     = "GitHubActionsOIDC"
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [local.github_oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values   = local.github_environment_subjects
    }
  }
}

resource "aws_iam_role" "application_release" {
  name               = var.role_name
  assume_role_policy = data.aws_iam_policy_document.github_trust.json

  description = "Least-privilege GitHub Actions role for RetainAI backend image releases."
}

data "aws_iam_policy_document" "application_release" {
  statement {
    sid       = "ECRAuthorization"
    effect    = "Allow"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }

  statement {
    sid    = "PushBackendImage"
    effect = "Allow"
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:CompleteLayerUpload",
      "ecr:DescribeImages",
      "ecr:InitiateLayerUpload",
      "ecr:PutImage",
      "ecr:UploadLayerPart",
    ]
    resources = [local.ecr_repository_arn]
  }

  statement {
    sid    = "UpdateLambdaImageOnly"
    effect = "Allow"
    actions = [
      "lambda:GetFunction",
      "lambda:GetFunctionConfiguration",
      "lambda:UpdateFunctionCode",
    ]
    resources = [local.lambda_function_arn]
  }
}

resource "aws_iam_role_policy" "application_release" {
  name   = "retainai-application-image-release"
  role   = aws_iam_role.application_release.id
  policy = data.aws_iam_policy_document.application_release.json
}
