# RetainAI Security and Cost Controls

> Sprint 7 principle: no AI provider call should happen before auth, quota and logging controls.

---

## 1. Security Boundary

```text
Cloud Run does not call Bedrock or Gemini directly.
The browser never receives AI provider keys.
All AI calls go through AWS Lambda.
```

The backend owns:

```text
auth validation
quota enforcement
prompt policy
provider routing
logging
redaction
```

---

## 2. Cross-Cloud Backend Access

Sprint 7 MVP:

```text
Cloud Run dashboard
  ↓ server-side request
AWS API Gateway HTTP API
  ↓ Lambda Authorizer or token validation
AWS Lambda FastAPI backend
```

Accepted alternatives:

```text
API Gateway HTTP API + Lambda Authorizer:
  recommended MVP.

Lambda Function URL + AWS_IAM:
  stronger, but more complex for cross-cloud request signing.

API key only:
  not enough by itself. Use only with additional validation/quota.

Private cross-cloud networking:
  future option, not Sprint 7.
```

---

## 3. AI Quota

Requirement:

```text
Limit AI model usage to 3 queries per user/IP.
```

MVP quota:

```text
3 AI-backed requests per IP per 24-hour window.
```

DynamoDB table:

```text
retainai-ai-usage-quota

Partition key:
  quota_key = hash(ip + provider + endpoint_group)

Attributes:
  request_count
  quota_limit
  window_start
  expires_at
```

Default AI mode:

```text
RETAINAI_AI_PROVIDER=disabled
```

---

## 4. Provider Cost Guardrails

Bedrock and Gemini must stay disabled until:

```text
[ ] backend auth is active;
[ ] quota logic is implemented;
[ ] CloudWatch logging is available;
[ ] provider keys are stored securely;
[ ] prompt templates are reviewed;
[ ] redaction rules are defined.
```

---

## 5. Secret Handling

Do not commit:

```text
AWS keys
GCP service account JSON files
Gemini API keys
Bedrock credentials
backend tokens
.env files with secrets
```

Store:

```text
Cloud Run backend token:
  Google Secret Manager

AWS backend/runtime secrets:
  AWS Secrets Manager or SSM Parameter Store

GitHub cloud access:
  OIDC / Workload Identity Federation, not long-lived keys
```

---

## 6. Logging Rules

Log metadata, not sensitive raw content.

Allowed:

```text
request id
provider
quota key hash
model/provider selected
latency
status code
token/cost estimate if available
```

Avoid:

```text
raw employee records
raw resumes
full prompt with personal data
provider API keys
sensitive HR attributes
```
