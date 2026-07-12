# RetainAI Vector Store Strategy

> Sprint 7.2 — RAG Document Generation Foundation  
> Current decision: generate local RAG evidence documents first, then build FAISS + S3 vector index in Sprint 7.3.

---

## 1. Decision

RetainAI should not start with a managed production vector database.

Recommended strategy:

```text
Sprint 7.2:
  Generate local RAG evidence documents from model artifacts, reports and SHAP/explainability outputs.

Sprint 7.3:
  Build FAISS + S3 vector index foundation.

Managed future:
  Bedrock Knowledge Base + S3 Vectors.

Future only:
  Aurora pgvector.
  OpenSearch Serverless.
```

---

## 2. Why Documents Before Vectors

Do not vectorize raw SHAP objects directly.

Instead:

```text
model registry / metrics / reports / SHAP outputs
  ↓
structured markdown evidence documents
  ↓
document manifest
  ↓
embedding job
  ↓
FAISS + S3 vector index
  ↓
retrieval context pack
```

This gives the Retention Advisor traceable evidence instead of opaque arrays.

---

## 3. Local Output Contract

Local RAG documents:

```text
artifacts/rag/documents/
  responsible_use_policy.md
  model_registry_evidence.md
  report_*.md
  explanation_*.md
  global_drivers_*.md
```

Local manifest:

```text
artifacts/rag/manifest.json
```

The responsible-use document is mandatory.

---

## 4. S3 Output Contract

S3 RAG documents:

```text
s3://retainai-<env>-data/model-artifacts/rag/documents/
```

S3 FAISS vector index:

```text
s3://retainai-<env>-data/model-artifacts/rag/vector-index/faiss/
  index.faiss
  documents.jsonl
  metadata.json
  manifest.json
```

---

## 5. Vector Store Options

### FAISS + S3

```text
Status:
  MVP connector

Reason:
  lowest-cost, no always-on database, good for small portfolio evidence corpus.
```

### Bedrock Knowledge Base + S3 Vectors

```text
Status:
  managed AWS future connector

Reason:
  managed retrieval path once the evidence corpus and usage pattern justify it.
```

### Aurora pgvector

```text
Status:
  future option only

Use if:
  RetainAI needs relational joins and vector search together.
```

### OpenSearch Serverless

```text
Status:
  future option only

Use if:
  RetainAI needs production-grade hybrid search or larger retrieval workloads.
```

---

## 6. Runtime Boundary

```text
Cloud Run does not call Bedrock or Gemini directly.
The browser never receives AI provider keys.
AWS Lambda owns retrieval, quota, prompt policy, logging and provider routing.
AI providers remain disabled by default.
```
