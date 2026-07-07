# RetainAI Vector Store Strategy

> Sprint 7 decision: start with FAISS + S3 as the low-cost MVP vector connector, and design for Bedrock Knowledge Base + S3 Vectors as the managed AWS connector.

---

## 1. Decision

RetainAI should not start with a managed production vector database.

Recommended Sprint 7 strategy:

```text
MVP:
  FAISS + S3 serialized vector index

Managed future:
  Bedrock Knowledge Base + S3 Vectors

Future only:
  Aurora pgvector
  OpenSearch Serverless
```

---

## 2. Why FAISS + S3 First

FAISS + S3 is the cheapest and simplest way to prove the RAG flow:

```text
SHAP/model artifacts
  ↓
explanation documents
  ↓
embedding job
  ↓
FAISS index
  ↓
S3 artifact storage
  ↓
Lambda retrieval
```

Expected artifact layout:

```text
s3://retainai-<env>-data/model-artifacts/vector-index/faiss/
  index.faiss
  documents.jsonl
  metadata.json
  manifest.json
```

Pros:

```text
- no always-on vector database;
- low cost;
- easy to regenerate after training;
- provider-neutral;
- can work with Bedrock, Gemini, or disabled mode.
```

Cons:

```text
- index must be rebuilt when documents change;
- FAISS native dependency must be included in the Lambda container;
- not ideal for large production multi-tenant RAG.
```

---

## 3. Bedrock Knowledge Base + S3 Vectors

Bedrock Knowledge Base + S3 Vectors is the managed AWS path.

Use later when:

```text
- explanation documents grow;
- managed ingestion is preferred;
- retrieval should be less custom;
- AWS-native RAG becomes a portfolio priority.
```

Sprint 7 should design the connector interface, but not require provisioning the managed vector layer immediately.

---

## 4. Aurora pgvector

Aurora pgvector is not the default for Sprint 7.

Use later only if RetainAI needs:

```text
- relational joins and vector search together;
- SQL-heavy filtering;
- a long-running production database;
- PostgreSQL operational capabilities.
```

Concern:

```text
Even with serverless features, Aurora is still database infrastructure.
It introduces storage, I/O, VPC, secrets, connection management and potential cold-resume behavior.
```

---

## 5. OpenSearch Serverless

OpenSearch Serverless is not the default for Sprint 7.

Use later only if RetainAI needs:

```text
- production-grade search;
- hybrid lexical + vector retrieval;
- larger query volumes;
- more advanced search features.
```

Concern:

```text
It is more operationally complex than FAISS/S3 or S3 Vectors for a small portfolio RAG corpus.
```

---

## 6. Configuration Contract

Recommended config:

```yaml
rag:
  enabled: false
  vector_store: disabled
  embedding_provider: disabled
  advisor_provider: disabled

  faiss_s3:
    bucket: retainai-dev-data
    prefix: model-artifacts/vector-index/faiss/

  bedrock_knowledge_base:
    knowledge_base_id: null
    retrieval_top_k: 5
```

Environment variables:

```text
RAG_VECTOR_STORE=disabled
RAG_VECTOR_STORE=faiss_s3
RAG_VECTOR_STORE=bedrock_kb

RETAINAI_EMBEDDING_PROVIDER=disabled
RETAINAI_EMBEDDING_PROVIDER=bedrock_titan
RETAINAI_EMBEDDING_PROVIDER=gemini

RETAINAI_AI_PROVIDER=disabled
RETAINAI_AI_PROVIDER=bedrock
RETAINAI_AI_PROVIDER=gemini
```

Default:

```text
RAG_VECTOR_STORE=disabled
RETAINAI_EMBEDDING_PROVIDER=disabled
RETAINAI_AI_PROVIDER=disabled
```

---

## 7. What Gets Vectorized

Do not vectorize raw SHAP arrays directly.

Vectorize explanation documents generated from:

```text
artifacts/explanations/<model>/feature_importance.parquet
artifacts/explanations/<model>/metadata.json
artifacts/explanations/samples/*.json
artifacts/reports/explainability_report_<model>.md
artifacts/reports/classification_report.md
artifacts/reports/survival_report.md
artifacts/models/model_registry.json
```

Generated documents:

```text
artifacts/rag/documents/
  model_card_logistic_regression.md
  model_card_random_forest.md
  global_drivers_xgboost.md
  survival_retention_summary.md
  local_explanation_sample_001.md
  responsible_use_policy.md
```
