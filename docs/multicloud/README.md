# Multicloud Delivery

## Table of contents

- [Topology](#topology)
- [Domains](#domains)
- [GCP dashboard](#gcp-dashboard)
- [AWS backend](#aws-backend)
- [Authentication and quota](#authentication-and-quota)
- [Infrastructure as code](#infrastructure-as-code)
- [Application delivery](#application-delivery)
- [Cost controls](#cost-controls)
- [Operational validation](#operational-validation)

## Topology

```mermaid
flowchart TD
    Browser --> CloudRun[Cloud Run]
    CloudRun --> APIDomain[API custom domain]
    APIDomain --> Gateway[API Gateway]
    Gateway --> Lambda
    Lambda --> DynamoDB
```

## Domains

```text
retainai.hubertronald.dev
  → Cloud Run direct domain mapping

api.retainai.hubertronald.dev
  → API Gateway Regional custom domain
```

## GCP dashboard

```text
project: coplayground
region: us-east4
service: retainai-dashboard
Artifact Registry: retainai-dashboard
secret: retainai-backend-token
```

No external GCP load balancer is used.

## AWS backend

```text
region: us-east-1
API Gateway HTTP API
Lambda container
ECR repository
DynamoDB quota table
ACM certificate
```

No Route 53, CloudFront, or AWS load balancer is required.

## Authentication and quota

```text
Cloud Run reads token from Secret Manager
Cloud Run sends token server-side
Lambda validates token
DynamoDB enforces quota
AI remains disabled by default
```

## Infrastructure as code

Terraform is the only active IaC implementation:

```text
infra/aws-terraform
infra/gcp-terraform
```

Pulumi is not part of the current architecture.

## Application delivery

Dashboard:

```bash
IMAGE_TAG="<immutable-tag>"   ./scripts/deploy_dashboard_cloud_run.sh
```

Infrastructure:

```bash
terraform plan -out=/tmp/reviewed.tfplan
terraform apply /tmp/reviewed.tfplan
```

Routine image delivery must not apply Terraform.

## Cost controls

```text
Cloud Run minimum = 0
Cloud Run service maximum = 1
Cloud Run revision maximum = 1
Lambda request-driven
AI disabled
quota enabled
```

## Operational validation

```bash
curl -sS https://api.retainai.hubertronald.dev/health
dig +short CNAME retainai.hubertronald.dev
dig +short CNAME api.retainai.hubertronald.dev
```

## Related guides

- [Architecture](../architecture/README.md)
- [Dashboard](../dashboard/README.md)
- [MLOps](../mlops/README.md)
- [Documentation index](../README.md)
