# RetainAI Data Lake Orchestration Strategy

> Sprint 7.1 — document the target orchestration path without implementing full production ETL.

## 1. Current State

Current RetainAI processing remains local:

```text
data/raw/
  ↓
data/processed/
  ↓
data/train/
data/validation/
data/test/
  ↓
artifacts/models/
artifacts/explanations/
artifacts/reports/
```

## 2. Sprint 7.1 MVP

Sprint 7.1 should deliver:

```text
documentation
zone mapping module
manifest module
safe config files
manual seed path
```

It should not require:

```text
AWS login
GCP login
Pulumi up
Glue job execution
Athena table creation
Step Functions deployment
```

## 3. Future Preferred Orchestration

```text
Manual trigger or EventBridge schedule
  ↓
Step Functions state machine
  ↓
Ingestion step
  ├── Kaggle seed Lambda / container task
  └── future HR file arrival from S3 upload
  ↓
Validation Lambda
  ↓
Glue Job: raw -> staging
  ↓
Glue Job: staging -> analytics/features
  ↓
Glue Crawler / Glue Catalog update
  ↓
Athena external tables
  ↓
Training / scoring / dashboard / RAG evidence generation
```

## 4. Step Functions vs Glue Workflow

Use Step Functions when:

```text
multiple services must be coordinated;
retries and branching logic matter;
validation Lambdas and Glue jobs need sequencing;
training and RAG document generation become part of the pipeline;
portfolio visibility of orchestration is valuable.
```

Use Glue Workflow when:

```text
the pipeline is mostly Glue jobs and crawlers;
the data lake becomes Glue-centered;
minimal custom orchestration is needed.
```

Sprint 7.1 decision:

```text
Step Functions is the preferred future orchestration story.
Glue Workflow is documented as an AWS-native alternative for Glue-heavy ETL.
Full ETL orchestration is not required to close Sprint 7.1.
```

## 5. Observability

Future orchestration should emit:

```text
input dataset version
row counts
schema validation results
null rate summary
output S3 prefixes
Glue job run ids
Athena table update status
model artifact manifest references
RAG document manifest references
```

Recommended destination:

```text
s3://retainai-<env>-data/monitoring/data-lake-runs/
```
