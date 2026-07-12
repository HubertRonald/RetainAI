# RetainAI S3 Data Lake Strategy

> Sprint 7.1 — Data Lake Contract and S3 Seed Foundation

## 1. Decision

RetainAI uses AWS S3 as the first cloud data lake and artifact backbone.

Sprint 7.1 defines the data lake contract. It does not require full Glue ETL, Athena tables, Step Functions orchestration, or cloud deployment.

## 2. Bucket Convention

```text
s3://retainai-<env>-data/
```

Examples:

```text
s3://retainai-dev-data/
s3://retainai-prod-data/
```

## 3. S3 Zones

```text
s3://retainai-<env>-data/
  raw/
  staging/
  analytics/
  features/
  model-artifacts/
  monitoring/
  dashboard-exports/
```

| Zone | Responsibility |
|---|---|
| `raw/` | Original source data, unchanged. |
| `staging/` | Validated, typed and lightly standardized data. |
| `analytics/` | Curated dashboard-ready datasets. |
| `features/` | Training, validation and test feature matrices. |
| `model-artifacts/` | Models, metrics, MLflow exports, SHAP outputs, reports, RAG documents and vector indexes. |
| `monitoring/` | Feature drift, prediction drift, scoring logs and retraining signals. |
| `dashboard-exports/` | User-facing downloadable predictions, summaries and reports. |

## 4. Local to S3 Mapping

| Local path | S3 path |
|---|---|
| `data/raw/` | `s3://retainai-<env>-data/raw/` |
| `data/processed/` | `s3://retainai-<env>-data/analytics/processed/` |
| `data/train/` | `s3://retainai-<env>-data/features/train/` |
| `data/validation/` | `s3://retainai-<env>-data/features/validation/` |
| `data/test/` | `s3://retainai-<env>-data/features/test/` |
| `data/prediction_input/` | `s3://retainai-<env>-data/raw/prediction-input/` |
| `artifacts/models/` | `s3://retainai-<env>-data/model-artifacts/models/` |
| `artifacts/explanations/` | `s3://retainai-<env>-data/model-artifacts/explanations/` |
| `artifacts/reports/` | `s3://retainai-<env>-data/model-artifacts/reports/` |
| `artifacts/figures/` | `s3://retainai-<env>-data/model-artifacts/figures/` |
| `artifacts/dashboard/` | `s3://retainai-<env>-data/dashboard-exports/` |
| `artifacts/rag/` | `s3://retainai-<env>-data/model-artifacts/rag/` |

## 5. Manual S3 Seed Path

Do not run S3 commands until AWS credentials are active and the target bucket exists.

Dry run first:

```bash
aws s3 sync data/raw/ \
  s3://retainai-dev-data/raw/ \
  --delete \
  --dryrun
```

Seed commands after review:

```bash
aws s3 sync data/raw/ s3://retainai-dev-data/raw/ --delete
aws s3 sync data/processed/ s3://retainai-dev-data/analytics/processed/ --delete
aws s3 sync data/train/ s3://retainai-dev-data/features/train/ --delete
aws s3 sync data/validation/ s3://retainai-dev-data/features/validation/ --delete
aws s3 sync data/test/ s3://retainai-dev-data/features/test/ --delete
aws s3 sync artifacts/models/ s3://retainai-dev-data/model-artifacts/models/ --delete
aws s3 sync artifacts/explanations/ s3://retainai-dev-data/model-artifacts/explanations/ --delete
aws s3 sync artifacts/reports/ s3://retainai-dev-data/model-artifacts/reports/ --delete
aws s3 sync artifacts/rag/ s3://retainai-dev-data/model-artifacts/rag/ --delete
```

## 6. Security Rules

Do not commit:

```text
Kaggle CSV dataset
Kaggle API tokens
AWS credentials
GCP service account JSON files
.env files with secrets
```

## 7. Relationship With RAG

```text
model-artifacts/
  ├── models/
  ├── explanations/
  ├── reports/
  └── rag/
      ├── documents/
      └── vector-index/
```

FAISS + S3 MVP path:

```text
s3://retainai-<env>-data/model-artifacts/rag/vector-index/faiss/
  index.faiss
  documents.jsonl
  metadata.json
  manifest.json
```
