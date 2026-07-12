# RetainAI FAISS + S3 Vector Store

> Sprint 7.3 — FAISS + S3 Connector Foundation

## 1. Decision

RetainAI uses **FAISS + S3** as the low-cost MVP vector-store connector.

```text
RAG evidence documents
  ↓
local embedding job
  ↓
local FAISS-compatible index
  ↓
S3 serialized vector index
  ↓
AWS Lambda retrieval
```

This avoids provisioning a managed vector database before the evidence corpus and retrieval behavior are stable.

## 2. Local Index Layout

```text
artifacts/rag/vector-index/faiss/
  index.faiss
  index.json
  documents.jsonl
  metadata.json
  manifest.json
```

`index.faiss` is written only when `faiss-cpu` is installed. `index.json` is always written as fallback.

## 3. S3 Upload Path

```text
s3://retainai-<env>-data/model-artifacts/rag/vector-index/faiss/
```

Development example:

```text
s3://retainai-dev-data/model-artifacts/rag/vector-index/faiss/
```

Dry run:

```bash
aws s3 sync artifacts/rag/vector-index/faiss/ \
  s3://retainai-dev-data/model-artifacts/rag/vector-index/faiss/ \
  --delete \
  --dryrun
```

Actual upload:

```bash
aws s3 sync artifacts/rag/vector-index/faiss/ \
  s3://retainai-dev-data/model-artifacts/rag/vector-index/faiss/ \
  --delete
```

Do not run S3 commands until AWS credentials are active and the bucket exists.

## 4. Build Command

```bash
python -m modules.rag.build_faiss_index \
  --documents-path artifacts/rag/documents \
  --index-path artifacts/rag/vector-index/faiss \
  --s3-prefix s3://retainai-dev-data/model-artifacts/rag/vector-index/faiss/
```

## 5. Local Retrieval Smoke Test

```bash
python - <<'PY'
from modules.rag.faiss_store import FaissS3VectorStore

store = FaissS3VectorStore(index_path="artifacts/rag/vector-index/faiss")
print("backend:", store.backend)

results = store.search("What are the main retention risk drivers?", top_k=3)

for result in results:
    print(result.score, result.document_id, result.title)
PY
```

`backend: faiss` and `backend: numpy_fallback` are both acceptable for Sprint 7.3 local validation.

## 6. Runtime Boundary

```text
Cloud Run does not load the vector index directly.
The browser never receives vector artifacts.
AWS Lambda owns retrieval, quota, prompt policy, logging and provider routing.
AI providers remain disabled by default.
```

## 7. Future Managed Connector

Future managed option:

```text
Bedrock Knowledge Base + S3 Vectors
```

Not Sprint 7.3 default:

```text
Aurora pgvector
OpenSearch Serverless
```
