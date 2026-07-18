# RetainAI — Sprint 7.6.1: Custom Domain, DNS and Managed HTTPS

## Final architecture

```text
hubertronald.dev
www.hubertronald.dev
  → GitHub Pages

retainai.hubertronald.dev
  → CNAME ghs.googlehosted.com
  → Cloud Run direct domain mapping
  → retainai-dashboard in us-east4

RetainAI backend
  → existing API Gateway execute-api endpoint
  → Lambda container
```

## Not used

```text
GCP global external Application Load Balancer
serverless NEG
global reserved IP
forwarding rules
target proxies
URL maps
Cloud CDN
Cloud Armor
AWS custom API domain
Route 53
CloudFront
AWS Load Balancer
```

## Namecheap

| Type | Host | Value | TTL |
|---|---|---|---|
| CNAME Record | `retainai` | `ghs.googlehosted.com` | Automatic |

Do not create an A record for `retainai`.

## MVP cost and security controls

```text
Cloud Run minimum instances = 0
Cloud Run maximum instances = 1
AI provider disabled by default
RAG disabled
vector store disabled
backend bearer-token validation enabled
DynamoDB quota enabled
```

## AWS backend

The dashboard keeps the existing API Gateway endpoint returned by:

```bash
terraform \
  -chdir=/workspace/infra/aws-terraform \
  output -raw api_endpoint
```

`api.retainai.hubertronald.dev` is deferred.

## Validation

```bash
dig +short CNAME retainai.hubertronald.dev

gcloud beta run domain-mappings describe \
  --domain=retainai.hubertronald.dev \
  --region=us-east4 \
  --project=coplayground \
  --format='yaml(status.conditions,status.resourceRecords)'

curl -sSIL \
  https://retainai.hubertronald.dev \
  | head -20
```
