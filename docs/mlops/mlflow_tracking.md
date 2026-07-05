# MLflow Tracking and Model Versioning

## Purpose

RetainAI uses MLflow to track classification experiments and version model artifacts.

MLflow tracking is used for:

- experiment runs;
- parameters;
- metrics;
- model artifacts;
- model signatures;
- input examples;
- report artifacts;
- optional local model registration.

## Configuration

MLflow is configured in:

```text
configs/training.yaml
```

Expected section:

```yaml
classification:
  mlflow:
    enabled: true
    experiment_name: retainai-classification
    tracking_uri: artifacts/mlflow
    registry_enabled: true
    registered_model_prefix: retainai
    log_model_signature: true
    log_input_example: true
```

## Training with MLflow

```bash
python -m retainai.training.train_classification
```

This generates:

```text
artifacts/models/<model_name>.pkl
artifacts/models/model_registry.json
artifacts/reports/classification_metrics.csv
artifacts/reports/classification_report.md
artifacts/reports/classification_metadata.json
artifacts/mlflow/
```

## Opening the MLflow UI

```bash
mlflow ui --backend-store-uri artifacts/mlflow --port 5000
```

Then open:

```text
http://localhost:5000
```

## Model Versioning Strategy

RetainAI uses two complementary model versioning layers.

### 1. MLflow run and model artifacts

Each training execution creates an MLflow run per model.

Logged information includes:

- model name;
- target;
- positive class;
- training and validation row counts;
- classification metrics;
- local pickle artifact;
- MLflow sklearn model artifact;
- model signature and input example when available.

### 2. Local model registry manifest

RetainAI also writes a lightweight registry manifest:

```text
artifacts/models/model_registry.json
```

This manifest is designed for dashboard/API inspection and records:

- model name;
- local artifact path;
- MLflow run ID;
- registered model name;
- metrics;
- creation timestamp.

## Registered Model Names

When registry mode is enabled, models are logged with names like:

```text
retainai_logistic_regression
retainai_random_forest
retainai_xgboost
```

## Responsible Use

The registry tracks technical model versions. It does not imply that a model is production-approved.

Production readiness should require additional validation, drift analysis, monitoring and governance review.
