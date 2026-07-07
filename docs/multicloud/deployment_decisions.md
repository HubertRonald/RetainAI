# RetainAI Sprint 7 Deployment Decisions

> Sprint 7 final decision set.

---

## 1. Runtime Decisions

```text
Dashboard:
  Google Cloud Run

Backend:
  AWS Lambda container image

Backend entrypoint:
  AWS API Gateway HTTP API + Lambda Authorizer

Backend fallback:
  Lambda Function URL + AWS_IAM
```

---

## 2. Data and Artifact Decisions

```text
Primary artifact/data storage:
  AWS S3

Model artifacts:
  s3://retainai-<env>-data/model-artifacts/

Dashboard exports:
  s3://retainai-<env>-data/dashboard-exports/

Monitoring outputs:
  s3://retainai-<env>-data/monitoring/
```

---

## 3. RAG Decisions

```text
Low-cost MVP vector store:
  FAISS + S3

Managed future vector store:
  Bedrock Knowledge Base + S3 Vectors

Future only:
  Aurora pgvector
  OpenSearch Serverless
```

---

## 4. AI Provider Decisions

```text
Default:
  disabled

AWS provider:
  Bedrock

GCP provider:
  Gemini

Provider routing:
  owned by AWS Lambda backend
```

Hard boundary:

```text
Cloud Run does not call Bedrock or Gemini directly.
The browser never receives provider credentials.
```

---

## 5. CI/CD Decisions

```text
Workflow:
  .github/workflows/multicloud-release.yml

Trigger:
  workflow_dispatch only

Branch:
  main only

Modes:
  preview
  release

Deploy flag:
  deploy_to_cloud=true required for release
```

No automatic execution on:

```text
pull_request
push
documentation changes
```

---

## 6. Deferred Decisions

Deferred from Sprint 7:

```text
AWS App Runner deployment target.
ECS/Fargate service deployment.
Kubernetes / Anthos.
Full Bedrock production integration.
Full Gemini production integration.
Production Aurora pgvector.
Production OpenSearch Serverless.
Public unauthenticated AI endpoint.
Custom domain as a blocker.
Full Glue ETL jobs.
Full Athena semantic model.
```

Clarification:

```text
ECS/Fargate is not required for Lambda Docker.
Lambda Docker means Docker image -> ECR -> Lambda.
```
