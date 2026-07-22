# Dashboard

## Table of contents

- [Purpose](#purpose)
- [Application structure](#application-structure)
- [Runtime contract](#runtime-contract)
- [Branding and footer](#branding-and-footer)
- [Container build](#container-build)
- [Cloud Run deployment](#cloud-run-deployment)
- [Scaling](#scaling)
- [Validation](#validation)
- [Internationalization readiness](#internationalization-readiness)

## Purpose

The Streamlit dashboard presents retention signals, evidence, validation
reports, and advisor output.

## Application structure

```text
apps/dashboard/streamlit-app/
services/dashboard/Dockerfile
.streamlit/
```

Reusable layout and rendering concerns should remain separate from data access
and backend communication.

## Runtime contract

```text
RETAINAI_DASHBOARD_MODE=api
RETAINAI_API_PROVIDER=aws-lambda
RETAINAI_API_URL=https://api.retainai.hubertronald.dev
RETAINAI_BACKEND_TOKEN=<Secret Manager reference>
RETAINAI_AI_PROVIDER=disabled
RETAINAI_ENABLE_RAG=false
RETAINAI_VECTOR_STORE=disabled
```

## Branding and footer

Application footer:

```text
Designed and built with ♥ and AI assistance by Hubert Ronald
© 2026 RetainAI — All rights reserved
```

RetainAI is attributed directly to Hubert Ronald. Liasoft remains a separate
creative brand.

## Container build

Canonical Dockerfile:

```text
services/dashboard/Dockerfile
```

Build context:

```text
repository root
```

## Cloud Run deployment

```bash
IMAGE_TAG="<immutable-tag>"   ./scripts/deploy_dashboard_cloud_run.sh
```

The script builds, pushes, and deploys a new revision without applying
Terraform.

## Scaling

```text
minimum instances = 0
service maximum = 1
revision maximum = 1
```

Every deployment must preserve those values.

## Validation

```bash
curl -sSIL https://retainai.hubertronald.dev
```

```bash
gcloud run services describe   retainai-dashboard   --project=coplayground   --region=us-east4   --format=json
```

## Internationalization readiness

User-facing text should move into locale catalogs before v1.0:

```text
locales/en.json
locales/es.json
```

Rendering components should consume stable message keys rather than hard-coded
English or Spanish text.

## Related guides

- [Architecture](../architecture/README.md)
- [Multicloud](../multicloud/README.md)
- [Prompts](../prompts/README.md)
- [Documentation index](../README.md)

<!-- retainai:dashboard-contract:start -->

## Dashboard contract

The RetainAI dashboard consolidates the product-facing views and the runtime
integration contract in one place.

### Application pages

The dashboard exposes four primary product pages:

1. **Executive Overview**  
   Executive-level retention indicators, risk summaries, and decision context.

2. **Prediction Center**  
   Employee-level prediction workflows and model-assisted retention analysis.

3. **Explainability Explorer**  
   SHAP-based feature attribution and explanation views for model decisions.

4. **Survival Analytics**  
   Time-to-event and retention-horizon analysis.

### API domains

The dashboard consumes the branded RetainAI backend through these API domains:

```text
/api/v1/overview
/api/v1/predict
/api/v1/explainability
/api/v1/survival
```

The production API base URL is:

```text
https://api.retainai.hubertronald.dev
```

### Runtime modes

The dashboard contract recognizes four runtime modes:

| Mode | Purpose |
|---|---|
| `local` | Local development using local files and local execution. |
| `api` | Dashboard integration with the deployed RetainAI API. |
| `s3` | Data or artifact access through Amazon S3-backed workflows. |
| `aws` | AWS-oriented runtime integrations, including Lambda and related services. |

The currently deployed dashboard uses the `api` mode against the branded
backend. The `local`, `s3`, and `aws` modes remain documented compatibility and
evolution paths for development, artifacts, and cloud integrations.

<!-- retainai:dashboard-contract:end -->
