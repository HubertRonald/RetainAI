# RetainAI AWS Lambda Backend

> Sprint 7.5 — AWS Lambda Backend Container  
> Runtime: AWS Lambda container image  
> Registry: Amazon ECR  
> Entry point: API Gateway HTTP API  
> IaC: Terraform, not Pulumi

## 1. Decision

RetainAI deploys the FastAPI backend as an AWS Lambda container image.

```text
Cloud Run dashboard
  ↓ server-side HTTPS request
AWS API Gateway HTTP API
  ↓
AWS Lambda container backend
  ↓
FastAPI app through Mangum
```

The backend owns auth/backend token guard, quota checks, prediction orchestration, explainability endpoints, RAG retrieval, future provider routing and CloudWatch logs.

## 2. FastAPI Lambda Adapter

Lambda adapter:

```text
apps/api/lambda_handler.py
```

Expected core shape:

```python
from mangum import Mangum
from apps.api.main import app

handler = Mangum(app)
```

RetainAI also adds a lightweight backend token guard for non-health endpoints.

Public endpoint:

```text
GET /health
```

Protected endpoints require one of:

```text
Authorization: Bearer <token>
x-retainai-backend-token: <token>
```

Runtime variables:

```text
RETAINAI_ENV=dev
RETAINAI_RUNTIME=aws-lambda
RETAINAI_BACKEND_AUTH_ENABLED=true
RETAINAI_BACKEND_TOKEN=<secret>
RETAINAI_AI_PROVIDER=disabled
RETAINAI_ENABLE_RAG=false
```

For local Lambda container smoke tests, you may set:

```text
RETAINAI_BACKEND_AUTH_ENABLED=false
```

## 3. Lambda Container Build

Build from repository root:

```bash
docker build \
  -f services/api-lambda/Dockerfile \
  -t retainai-api-lambda:local \
  .
```

The image uses:

```text
public.ecr.aws/lambda/python:3.10
```

and loads:

```text
apps.api.lambda_handler.handler
```

## 4. Local Lambda Runtime Smoke Test

Run the Lambda container locally:

```bash
docker run --rm \
  -p 9000:8080 \
  -e RETAINAI_ENV=dev \
  -e RETAINAI_RUNTIME=aws-lambda \
  -e RETAINAI_BACKEND_AUTH_ENABLED=false \
  -e RETAINAI_AI_PROVIDER=disabled \
  -e RETAINAI_ENABLE_RAG=false \
  retainai-api-lambda:local
```

In another terminal:

```bash
curl -sS \
  "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d '{
    "version": "2.0",
    "routeKey": "GET /health",
    "rawPath": "/health",
    "rawQueryString": "",
    "headers": {"host": "localhost"},
    "requestContext": {
      "http": {
        "method": "GET",
        "path": "/health",
        "protocol": "HTTP/1.1",
        "sourceIp": "127.0.0.1",
        "userAgent": "curl"
      }
    },
    "isBase64Encoded": false
  }'
```

Expected body includes:

```json
{"status":"ok"}
```

## 5. ECR Push

```bash
export AWS_PROFILE="retainai-dev"
export AWS_REGION="us-east-1"

export AWS_ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
export AWS_ECR_REPOSITORY="retainai-api-lambda"
export LAMBDA_IMAGE_TAG="sprint7-5"

export LAMBDA_IMAGE_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_REPOSITORY}:${LAMBDA_IMAGE_TAG}"
```

Authenticate Docker to ECR:

```bash
aws ecr get-login-password --region "${AWS_REGION}" \
  | docker login \
      --username AWS \
      --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
```

Tag and push:

```bash
docker tag retainai-api-lambda:local "${LAMBDA_IMAGE_URI}"
docker push "${LAMBDA_IMAGE_URI}"
```

## 6. Terraform Preview

```bash
cd infra/aws-terraform

terraform init
terraform fmt
terraform validate
terraform plan \
  -var="aws_region=${AWS_REGION}" \
  -var="lambda_image_uri=${LAMBDA_IMAGE_URI}" \
  -var="backend_token=dev-local-placeholder-token"

cd -
```

Do not run `terraform apply` unless intentionally deploying real AWS resources.

## 7. API Gateway Endpoint

Terraform creates:

```text
API Gateway HTTP API
Lambda proxy integration
$default route
$default stage
Lambda permission for API Gateway
```

Output:

```text
api_endpoint
health_url
```

Expected health URL after apply:

```text
https://<api-id>.execute-api.us-east-1.amazonaws.com/health
```

## 8. Security Boundary

Cloud Run calls the backend server-side only.

The browser must not receive AWS credentials, backend token, Bedrock credentials or Gemini API keys.

Backend token should later come from AWS Secrets Manager, CI/CD environment secrets, or a Terraform sensitive variable for dev-only testing.

Do not commit:

```text
terraform.tfvars
tfstate
.env files
backend tokens
AWS credentials
```
