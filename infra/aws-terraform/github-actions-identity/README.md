# RetainAI GitHub Actions AWS identity

This Terraform root creates the least-privilege IAM role used by the manual
application-release workflow.

It does not manage:

```text
API Gateway
ACM
DynamoDB
S3
Lambda configuration
ECR repository creation
Terraform state used by the runtime
```

The role can only push to one existing ECR repository and update the image URI
of one existing Lambda function.

When the account already has the GitHub OIDC provider, keep:

```hcl
create_github_oidc_provider = false
```

When the provider does not exist, review the plan and set it to `true`.

Because the workflow uses GitHub environments, the role trust policy permits
only these subjects by default:

```text
repo:HubertRonald/RetainAI:environment:dev
repo:HubertRonald/RetainAI:environment:prod
```
