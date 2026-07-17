# RetainAI Multi-Cloud Security and Cost Controls

> Sprint: 7.6 — Cross-Cloud Auth and Quota  
> Runtime path: Google Cloud Run dashboard → AWS API Gateway → AWS Lambda  
> Infrastructure as Code: Terraform only

## 1. Scope

Sprint 7.6 establishes the minimum cross-cloud trust and cost-control boundary before any Bedrock, Gemini, embedding, or RAG-backed endpoint can be enabled.

The control order is deliberate:

```text
Cloud Run retrieves backend token from GCP Secret Manager
  ↓
Cloud Run sends server-side Authorization: Bearer <token>
  ↓
AWS backend validates token with constant-time comparison
  ↓
AI provider must be explicitly enabled
  ↓
DynamoDB conditionally consumes quota
  ↓
Only then may an AI provider be called
```

The browser never receives the backend token. Cloud Run must make the AWS request from server-side Python code.

## 2. Default-deny behavior

The default runtime configuration remains:

```text
RETAINAI_AI_PROVIDER=disabled
RETAINAI_ENABLE_RAG=false
RETAINAI_VECTOR_STORE=disabled
RETAINAI_BACKEND_AUTH_ENABLED=true
RETAINAI_QUOTA_ENABLED=true
RETAINAI_QUOTA_BACKEND=dynamodb
RETAINAI_QUOTA_LIMIT=3
RETAINAI_QUOTA_WINDOW_SECONDS=86400
```

Expected responses:

| Condition | Status | Code |
|---|---:|---|
| `/health` | `200` | public health check |
| Protected route without valid token | `401` | `unauthorized` |
| Auth enabled but token missing in backend configuration | `503` | `auth_not_configured` |
| AI endpoint while provider is disabled | `503` | `ai_disabled` |
| Quota backend missing or unusable | `503` | `quota_unavailable` |
| Fourth AI request in the same window | `429` | `quota_exceeded` |

Quota failure is fail-closed. RetainAI must not call Bedrock or Gemini when the quota store is unavailable.

## 3. Token storage and delivery

### GCP side

Terraform creates the Secret Manager secret container and grants the Cloud Run service account:

```text
roles/secretmanager.secretAccessor
```

The secret value is added with `gcloud secrets versions add`; it is intentionally not placed in Terraform source or a Terraform variable so the GCP secret value does not enter Terraform state.

Cloud Run exposes the selected secret version to the container as:

```text
RETAINAI_BACKEND_TOKEN
```

Because the current service references `latest`, a new Cloud Run revision must be deployed after rotating the secret so new instances resolve the new value consistently.

### AWS side

For the Sprint 7.6 development foundation, Lambda receives the same token through the sensitive Terraform variable `backend_token` and exposes it as `RETAINAI_BACKEND_TOKEN`.

Important boundary:

```text
sensitive = true
```

redacts normal Terraform output, but it does not remove the value from Terraform state. Production hardening should move the AWS copy to AWS Secrets Manager or SSM Parameter Store and use encrypted remote Terraform state with restricted access.

## 4. Backend token validation

Protected routes accept either:

```http
Authorization: Bearer <token>
```

or the compatibility header:

```http
X-RetainAI-Backend-Token: <token>
```

The bearer form is preferred. Validation uses `hmac.compare_digest` to avoid ordinary string-comparison timing leakage.

Public paths are limited by default to:

```text
/health
/docs
/openapi.json
/redoc
```

The API root and business endpoints remain protected.

## 5. Three-query quota model

Sprint 7.6 uses a fixed-window quota:

```text
3 AI-backed requests
per client identity
per provider
per endpoint group
per 86,400-second window
```

The default AI path groups are:

```text
/advisor
/api/advisor
/ai
/rag
```

### Client identity

The backend resolves the client identifier in this order:

```text
1. X-RetainAI-Client-ID
2. X-RetainAI-Client-IP
3. first X-Forwarded-For value
4. request.client.host
```

Preferred production behavior is for Cloud Run to create and send a stable pseudonymous `X-RetainAI-Client-ID`. A server-side Cloud Run call may otherwise cause many browser users to share the same Cloud Run egress identity.

Do not trust a browser-supplied quota identity. The Cloud Run server should sanitize or derive it before calling AWS.

### Privacy

Raw client IPs and client IDs are not stored in DynamoDB. The backend hashes the client identity and the complete quota scope with SHA-256.

Conceptual key:

```text
quota_key = SHA256(client + provider + endpoint_group + window_start)
```

### Concurrency

The DynamoDB implementation uses one conditional `UpdateItem` operation:

```text
allow increment only when request_count does not exist or request_count < quota_limit
```

This prevents concurrent requests from incrementing beyond the configured limit. The fourth request receives HTTP `429`.

### TTL

Each item contains:

```text
expires_at = reset_at + quota_window_seconds
```

DynamoDB TTL uses Unix epoch seconds. TTL cleanup is asynchronous, so expired records can remain physically present for some time. Quota correctness does not depend on immediate deletion because every fixed window produces a different hashed partition key.

## 6. DynamoDB table

Terraform creates an environment-specific table by default:

```text
retainai-dev-ai-usage-quota
```

Schema:

```text
Partition key: quota_key (String)
Billing mode: PAY_PER_REQUEST
TTL attribute: expires_at
Encryption: enabled
Point-in-time recovery: enabled
```

Lambda receives only:

```text
dynamodb:GetItem
dynamodb:UpdateItem
```

for the quota table ARN.

## 7. Response headers

Allowed AI requests return:

```text
X-RateLimit-Limit
X-RateLimit-Remaining
X-RateLimit-Reset
```

Rejected quota requests additionally return:

```text
Retry-After
```

`X-RateLimit-Reset` is an epoch timestamp in seconds.

## 8. Secret rotation

Development rotation procedure:

```text
1. Generate a new random token locally.
2. Add a new GCP Secret Manager version.
3. Update the AWS Lambda backend token through Terraform.
4. Deploy a new Cloud Run revision so the environment variable resolves again.
5. Validate protected requests.
6. Disable old GCP secret versions after validation.
```

The current single-token MVP can have a brief mismatch during rotation. A future zero-downtime design can accept current and previous tokens for a bounded overlap or move to signed short-lived requests.

## 9. Future signature hardening

A future HMAC mode can sign:

```text
timestamp + HTTP method + path + SHA256(body)
```

with a short replay window. The signing material would remain in GCP Secret Manager and AWS Secrets Manager. This is deferred because Sprint 7.6 accepts protected-token validation as its MVP trust mechanism.

## 10. Cost controls

The following controls must remain in place before enabling AI:

```text
- AI provider disabled by default.
- RAG disabled by default.
- Quota check before provider invocation.
- DynamoDB on-demand billing.
- Lambda timeout and memory bounded by Terraform.
- Cloud Run maximum instances bounded for portfolio traffic.
- No provider key or backend token in browser code.
- CloudWatch and Cloud Run logging enabled.
```

A quota is an application cost guard, not a complete perimeter. API Gateway throttling, AWS WAF, Cloud Armor, anomaly alarms, budgets, and provider-side limits remain future defense-in-depth controls.

## 11. Validation checklist

```text
[ ] GCP Secret Manager secret exists.
[ ] Secret has at least one enabled version.
[ ] Cloud Run service account has Secret Accessor.
[ ] Cloud Run revision references RETAINAI_BACKEND_TOKEN from Secret Manager.
[ ] AWS Lambda validates the same token.
[ ] DynamoDB quota table is ACTIVE.
[ ] DynamoDB TTL is enabled on expires_at.
[ ] Lambda IAM permits only GetItem and UpdateItem on the table.
[ ] RETAINAI_AI_PROVIDER remains disabled after deployment.
[ ] Fourth direct quota consumption in one window is denied.
[ ] Raw client IP is not stored in DynamoDB.
```

## 12. Deferred controls

Not implemented in Sprint 7.6:

```text
- End-user identity system.
- JWT/OIDC authentication.
- Lambda authorizer.
- IAM SigV4 between Cloud Run and API Gateway.
- HMAC request signing and replay protection.
- AWS Secrets Manager runtime retrieval.
- AWS WAF or GCP Cloud Armor.
- Sliding-window quota.
- Distributed user/session identity service.
- Provider billing alarms and automatic circuit breakers.
```
