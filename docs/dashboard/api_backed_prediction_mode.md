# API-backed Prediction Mode

## Purpose

Prediction Center supports local prediction by default and can call the FastAPI service when configured.

## Environment Variables

```bash
RETAINAI_PREDICTION_MODE=api
RETAINAI_API_URL=http://api:8001
```

## Local Mode

```bash
RETAINAI_PREDICTION_MODE=local
```

Local mode loads model artifacts directly from:

```text
artifacts/models/
```

## API Mode

API mode calls RetainAI API and falls back to local mode if the API contract is unavailable.

## Future Work

- stabilize `/prediction/predict` contract;
- add schema validation;
- add API integration tests;
- add authentication hooks for cloud deployment.
