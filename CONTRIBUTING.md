# Contributing to RetainAI

## Principles

Preserve:

```text
explainability
human review
secret isolation
bounded cost
provider portability
language independence
reproducibility
```

## Documentation

Update the relevant conceptual guide:

```text
docs/architecture/README.md
docs/dashboard/README.md
docs/data/README.md
docs/eda/README.md
docs/modeling/README.md
docs/mlops/README.md
docs/multicloud/README.md
docs/prompts/README.md
```

Do not create permanent documents named after temporary iterations.

## Tests

```bash
python -m pytest -q --no-cov
```

## Terraform

```bash
terraform fmt
terraform validate
terraform plan -out=/tmp/reviewed.tfplan
terraform show -no-color /tmp/reviewed.tfplan
```

Never apply unexpected deletion or replacement.

Do not commit:

```text
terraform.tfvars
*.tfstate
*.tfplan
credentials
tokens
API keys
```

## Application deployment

```bash
IMAGE_TAG="<immutable-tag>"   ./scripts/deploy_dashboard_cloud_run.sh
```

Preserve:

```text
service max = 1
revision max = 1
revision min = 0
```

Application delivery must not run Terraform.

## Pull requests

Include:

```text
problem and scope
implementation summary
tests
infrastructure impact
security and cost impact
documentation impact
rollback notes
```

Do not claim psychometric validity or autonomous employment decisions without
appropriate evidence, data, governance, and review.
