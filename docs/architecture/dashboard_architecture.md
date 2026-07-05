# Dashboard Architecture

**Version:** v0.1  
**Status:** Draft  
**Sprint:** Sprint 6 — Dashboard  
**Repository:** RetainAI

## Overview

The Dashboard layer turns RetainAI analytical artifacts into an interactive decision intelligence experience for employee retention.

The dashboard must not own modeling, preprocessing, explainability, or survival logic. It consumes reusable modules, service/API layers, local artifacts, and future AWS adapters.

## Objectives

- historical attrition analytics;
- CSV/XLSX prediction workflow;
- explainability exploration;
- survival analysis visualization;
- local-first execution;
- API-ready execution;
- future AWS-ready connectors.

## User Experience

The dashboard has four analytical experiences:

1. Executive Overview
2. Prediction Center
3. Explainability Explorer
4. Survival Analytics

## Service/API Domains

One FastAPI service exposes separated routers:

```text
/api/v1/overview/*
/api/v1/predict/*
/api/v1/explainability/*
/api/v1/survival/*
```

## Adapter Strategy

```text
RETAINAI_RUNTIME=local
RETAINAI_RUNTIME=api
RETAINAI_RUNTIME=s3
RETAINAI_RUNTIME=aws
```

Sprint 6 implements local-first interfaces and placeholders for future AWS connectors.

## Local Data Sources

```text
data/processed/ibm_hr_attrition_processed.csv
data/prediction_input/ibm_hr_attrition_prediction_sample.csv
artifacts/models/logistic_regression.pkl
artifacts/reports/*.md
artifacts/figures/*
artifacts/explanations/*/metadata.json
```

## Deliverables

- dashboard architecture specification;
- service contract;
- data contract;
- mockup specification;
- mockup validation;
- Streamlit shell;
- FastAPI skeleton;
- Docker Compose local stack;
- validation notebook;
- dashboard validation report;
- unit and behavior tests.
