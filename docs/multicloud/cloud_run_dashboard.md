# RetainAI Cloud Run Dashboard

> Sprint 7.4 — Cloud Run Dashboard Container  
> Runtime decision: Google Cloud Run public Streamlit dashboard  
> Image registry: Google Artifact Registry  
> Backend: AWS Lambda container backend behind API Gateway or Lambda Function URL

---

## 1. Decision

RetainAI deploys the public Streamlit dashboard to Google Cloud Run.

```text
Users / Browser
  ↓
Google Cloud Run public dashboard
  ↓ server-side request only
AWS API Gateway or Lambda Function URL
  ↓
AWS Lambda FastAPI backend
```

The dashboard must not call Bedrock or Gemini directly. The browser must not receive backend secrets or AI provider keys.

---

## 2. Local Build Contract

Expected Dockerfile:

```text
services/dashboard/Dockerfile
```

Recommended build command from repository root:

```bash
docker build \
  -f services/dashboard/Dockerfile \
  -t retainai-dashboard:cloudrun \
  .
```

The build context should be the repository root so the dashboard can import local modules, app code and configuration files.

---

## 3. Runtime Environment Variables

Required runtime environment variables:

```text
RETAINAI_DASHBOARD_MODE=api
RETAINAI_API_PROVIDER=aws-lambda
RETAINAI_API_URL=<aws-api-gateway-or-lambda-url>
RETAINAI_AI_PROVIDER=disabled
```

Optional runtime variables:

```text
RETAINAI_ENV=dev
RETAINAI_LOG_LEVEL=INFO
RETAINAI_ENABLE_RAG=false
RETAINAI_VECTOR_STORE=disabled
```

---

## 4. Secret Handling

Do not bake secrets into the image.

Do not commit:

```text
backend API tokens
Gemini API keys
AWS credentials
GCP service account JSON files
.env files with secrets
```

Future secret path:

```text
Google Secret Manager
  ↓
Cloud Run secret environment variable
  ↓
server-side dashboard request to AWS backend
```

---

## 5. Artifact Registry Target

Recommended repository:

```text
retainai-dashboard
```

Image convention:

```text
<region>-docker.pkg.dev/<gcp-project-id>/retainai-dashboard/retainai-dashboard:<tag>
```

Development example:

```text
us-central1-docker.pkg.dev/<gcp-project-id>/retainai-dashboard/retainai-dashboard:sprint7-4
```

---

## 6. Local Build Validation

```bash
docker build \
  -f services/dashboard/Dockerfile \
  -t retainai-dashboard:cloudrun \
  .

docker image inspect retainai-dashboard:cloudrun >/dev/null
```

Optional local run:

```bash
docker run --rm \
  -p 8501:8501 \
  -e RETAINAI_DASHBOARD_MODE=api \
  -e RETAINAI_API_PROVIDER=aws-lambda \
  -e RETAINAI_API_URL=http://localhost:8001 \
  -e RETAINAI_AI_PROVIDER=disabled \
  retainai-dashboard:cloudrun
```

---

## 7. GCP Push Flow

Run only when GCP is intentionally active.

```bash
export GCP_PROJECT_ID="<your-gcp-project-id>"
export GCP_REGION="us-central1"
export GCP_ARTIFACT_REPOSITORY="retainai-dashboard"
export DASHBOARD_IMAGE_NAME="retainai-dashboard"
export DASHBOARD_IMAGE_TAG="sprint7-4"

export DASHBOARD_IMAGE_URI="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${GCP_ARTIFACT_REPOSITORY}/${DASHBOARD_IMAGE_NAME}:${DASHBOARD_IMAGE_TAG}"
```

```bash
gcloud auth login --no-launch-browser
gcloud auth application-default login --no-launch-browser
gcloud config set project "${GCP_PROJECT_ID}"
gcloud config set run/region "${GCP_REGION}"
```

```bash
gcloud artifacts repositories describe "${GCP_ARTIFACT_REPOSITORY}" \
  --location="${GCP_REGION}" \
  --project="${GCP_PROJECT_ID}" \
  >/dev/null 2>&1 || \
gcloud artifacts repositories create "${GCP_ARTIFACT_REPOSITORY}" \
  --repository-format=docker \
  --location="${GCP_REGION}" \
  --description="RetainAI dashboard container images"
```

```bash
gcloud auth configure-docker "${GCP_REGION}-docker.pkg.dev" --quiet

docker tag retainai-dashboard:cloudrun "${DASHBOARD_IMAGE_URI}"
docker push "${DASHBOARD_IMAGE_URI}"
```

---

## 8. Pulumi Preview Contract

Minimum stack config values:

```bash
pulumi config set gcp:project "${GCP_PROJECT_ID}"
pulumi config set gcp:region "${GCP_REGION}"
pulumi config set retainai:gcpProjectId "${GCP_PROJECT_ID}"
pulumi config set retainai:gcpRegion "${GCP_REGION}"
pulumi config set retainai:dashboardImageUri "${DASHBOARD_IMAGE_URI}"
pulumi config set retainai:dashboardApiUrl "https://placeholder-api.example.com"
pulumi config set retainai:dashboardAllowPublic true
```

Preview:

```bash
cd infra/multicloud-pulumi-python
pulumi stack select dev
pulumi preview
cd -
```

Do not run `pulumi up` unless intentionally deploying.

---

## 9. Acceptance Mapping

| Acceptance criterion | Validation |
|---|---|
| Dashboard image builds locally. | `docker build -f services/dashboard/Dockerfile -t retainai-dashboard:cloudrun .` |
| Image can be pushed to Artifact Registry. | `gcloud auth configure-docker`, `docker tag`, `docker push`. |
| Cloud Run service can be previewed by Pulumi. | `pulumi preview`. |
| Runtime env vars are defined. | `RETAINAI_DASHBOARD_MODE`, `RETAINAI_API_PROVIDER`, `RETAINAI_API_URL`, `RETAINAI_AI_PROVIDER`. |
| Secrets are not baked into image. | Dockerfile review confirms no hard-coded secret values. |
