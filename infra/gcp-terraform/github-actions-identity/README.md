# RetainAI GitHub Actions identity for Google Cloud

This directory is an independent Terraform root for GitHub Actions identity and
least-privilege deployment permissions.

It does not manage or replace the existing runtime root:

```text
infra/gcp-terraform/
```

It manages only:

```text
Workload Identity Pool
GitHub OIDC Provider
GitHub deployment service account
Workload Identity User binding
Artifact Registry repository-level writer binding
Cloud Run service-level developer binding
Cloud Run runtime service-account actAs binding
```

The existing resources are referenced by name through
`artifact_repository_id`, `dashboard_service_name`, and
`cloud_run_runtime_service_account_email`.

The root has its own local `terraform.tfvars`, separate from the parent runtime
root. Neither local file should be committed.
