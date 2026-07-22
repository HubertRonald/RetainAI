# RetainAI GitHub Actions Google Cloud identity

This Terraform root creates:

```text
Workload Identity Pool
GitHub OIDC provider restricted to HubertRonald/RetainAI and main
least-privilege deployment service account
Artifact Registry writer permission
Cloud Run developer permission
actAs permission for the existing Cloud Run runtime identity
```

It does not manage the Cloud Run service, domain mapping, secrets, Artifact
Registry repository, or application image.

No service-account key is created.
