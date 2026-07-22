# Manual multi-cloud application release

RetainAI promotes application images manually from the protected `main` branch.

```text
feature branch
  → pull request
  → main
  → workflow_dispatch
  → short-lived cloud identity
  → immutable image
  → Cloud Run and/or Lambda image update
```

The workflow does not run on pushes, pull requests, tags, schedules, or
documentation changes.

## Release scope

Dashboard-eligible changes include the dashboard application, shared runtime
modules, configuration, dependencies, and dashboard container definition.

Backend-eligible changes include the API application, Lambda adapter,
shared runtime modules, configuration, dependencies, and backend container
definition.

Changes limited to documentation, figures, Markdown, licenses, or citations do
not qualify for an application release.

## Cloud identity

AWS access uses GitHub OIDC and a role restricted to the RetainAI GitHub
environments. The role can push to one ECR repository and update one Lambda
function image.

Google Cloud access uses Workload Identity Federation restricted to the
`HubertRonald/RetainAI` repository and `main`. The deployment service account
can push dashboard images and update Cloud Run, but it cannot manage domains,
secrets, or infrastructure.

## Deployment markers

Successful deployments create immutable tags:

```text
deploy-dashboard-<environment>-<commit>
deploy-backend-<environment>-<commit>
```

The next manual run compares application paths against the latest successful
marker for the selected component and environment.

## Explicit exclusions

The workflow contains no Terraform, Pulumi, S3, or data-lake operations.
Application releases cannot recreate domains, certificates, IAM, secrets,
quotas, or data buckets.
