# RetainAI Multi-Cloud Credential Strategy

> Sprint 7 principle: use short-lived, federated credentials whenever possible.

---

## 1. Local DevContainer

The DevContainer should support:

```text
AWS CLI
gcloud CLI
Pulumi CLI
Docker CLI
Python 3.10
```

Local setup:

```bash
. ./.venv/bin/activate
```

AWS local auth:

```bash
aws sso login --profile retainai-dev
export AWS_PROFILE=retainai-dev
export AWS_REGION=us-east-1
```

GCP local auth:

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project <gcp-project-id>
gcloud config set run/region us-central1
```

Pulumi local auth:

```bash
pulumi login
pulumi stack select dev
pulumi preview
```

---

## 2. GitHub Actions

Use manual workflows only:

```yaml
on:
  workflow_dispatch:
```

Recommended cloud auth:

```text
AWS:
  GitHub OIDC -> AWS IAM Role

GCP:
  GitHub OIDC -> GCP Workload Identity Federation -> Service Account
```

Repository variables/secrets:

```text
AWS_REGION
AWS_ROLE_TO_ASSUME
GCP_PROJECT_ID
GCP_REGION
GCP_WORKLOAD_IDENTITY_PROVIDER
GCP_SERVICE_ACCOUNT
PULUMI_ACCESS_TOKEN
PULUMI_STACK
```

Avoid:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
GCP service account JSON
long-lived cloud keys
```

---

## 3. Secret Locations

Cloud Run:

```text
Google Secret Manager
```

Lambda/backend:

```text
AWS Secrets Manager
AWS SSM Parameter Store
Lambda environment variables for non-sensitive config only
```

Local development:

```text
.env.local
```

But `.env.local` must remain ignored by Git.

---

## 4. When AWS/GCP Must Be Active

Sprint 7.0 documentation:

```text
No AWS/GCP required.
```

Pulumi preview/up:

```text
AWS and/or GCP auth required.
```

Image push:

```text
AWS auth required for ECR.
GCP auth required for Artifact Registry.
```

Cloud deploy:

```text
AWS/GCP auth required.
Pulumi backend auth required.
```
