<p align="left">

<a href="https://www.python.org/" target="_blank">
<img src="https://img.shields.io/badge/Python-3.10.11-3670A0?style=flat-square&logo=python&logoColor=ffdd54" />
</a>
<a href="https://scikit-learn.org/" target="_blank">
<img src="https://img.shields.io/badge/scikit--learn-ML-orange?style=flat-square&logo=scikit-learn&logoColor=white" />
</a>
<a href="https://xgboost.readthedocs.io/" target="_blank">
<img src="https://img.shields.io/badge/XGBoost-Gradient%20Boosting-FF6600?style=flat-square" />
</a>
<a href="https://lifelines.readthedocs.io/" target="_blank">
<img src="https://img.shields.io/badge/Survival%20Analysis-lifelines-4B8BBE?style=flat-square" />
</a>
<a href="https://shap.readthedocs.io/" target="_blank">
<img src="https://img.shields.io/badge/SHAP-Explainability-8A2BE2?style=flat-square" />
</a>
<a href="https://mlflow.org/" target="_blank">
<img src="https://img.shields.io/badge/MLflow-Tracking-0194E2?style=flat-square&logo=mlflow&logoColor=white" />
</a>
<a href="https://fastapi.tiangolo.com/" target="_blank">
<img src="https://img.shields.io/badge/FastAPI-Serving-009688?style=flat-square&logo=fastapi&logoColor=white" />
</a>
<a href="https://streamlit.io/" target="_blank">
<img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" />
</a>
<a href="https://aws.amazon.com/" target="_blank">
<img src="https://img.shields.io/badge/AWS-Cloud-232F3E?style=flat-square&logo=amazonaws&logoColor=white" />
</a>
<a href="https://www.pulumi.com/" target="_blank">
<img src="https://img.shields.io/badge/Pulumi-Python%20IaC-8A3391?style=flat-square&logo=pulumi&logoColor=white" />
</a>
<a href="https://github.com/features/actions" target="_blank">
<img src="https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?style=flat-square&logo=githubactions&logoColor=white" />
</a>
<a href="https://www.docker.com/" target="_blank">
<img src="https://img.shields.io/badge/Docker-Containers-2496ED?style=flat-square&logo=docker&logoColor=white" />
</a>
<a href="./LICENSE" target="_blank">
<img src="https://img.shields.io/github/license/HubertRonald/RetainAI?style=flat-square&color=success" />
</a>
<a href="./CONTRIBUTING.md" target="_blank">
<img src="https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg" />
</a>
</p>

# RetainAI

> AI-ready Employee Retention Intelligence Platform

RetainAI is an AWS-native MLOps and analytics platform for employee retention intelligence.

The project combines:

- employee attrition prediction;
- survival analysis;
- model explainability;
- dashboard-driven decision support;
- MLOps lifecycle management;
- future AI capabilities based on resumes, psychometric assessments, RAG, and Amazon Bedrock.

The first public version uses the IBM HR Analytics Employee Attrition dataset from Kaggle as a reproducible benchmark dataset.

---

## Project Vision

RetainAI is designed as a Decision Intelligence System for Human Resources.

The platform evolves beyond traditional attrition prediction by incorporating:

- predictive analytics;
- retention intelligence;
- explainable machine learning;
- survival modeling;
- monitoring and drift detection;
- AI-assisted workforce analytics.

---

## Core Capabilities

### Classification

Predict whether an employee is likely to leave the organization.

### Survival Analysis

Estimate expected employee tenure and retention probability over time.

### Explainability

Understand which variables influence employee attrition risk.

### Dashboard Analytics

Provide HR stakeholders with actionable insights through an interactive Streamlit dashboard.

### MLOps

Enable reproducible training, experiment tracking, deployment, monitoring, and retraining workflows.

---

## Public Dataset

RetainAI uses the IBM HR Analytics Employee Attrition dataset as an initial benchmark.

Dataset:

https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset

This repository does not redistribute the dataset.

Users must download it directly from Kaggle.

Expected local structure:

```text
data/
└── raw/
    └── ibm_hr_attrition/
        └── WA_Fn-UseC_-HR-Employee-Attrition.csv
```

Download example:

```bash
mkdir -p data/raw/ibm_hr_attrition

kaggle datasets download \
  -d pavansubhasht/ibm-hr-analytics-attrition-dataset \
  -p data/raw/ibm_hr_attrition \
  --unzip
```

## Repository Structure

```text
retainai/
├── apps/
├── artifacts/
├── configs/
├── data/
├── docs/
├── figs/
├── infra/
├── modules/
├── notebooks/
├── requirements/
├── services/
├── src/
├── tests/
├── utils/
├── pyproject.toml
├── tox.ini
└── README.md
```

## Architecture

The detailed architecture specification is available in:

```text
docs/architecture/architecture_specification_v0.1.md
```

## Development Environment

The recommended development environment is:

- VS Code
- Dev Containers
- Docker
- Python 3.10

This approach ensures reproducibility across Linux, Windows, and macOS environments.

## Roadmap

### v0.1

- Repository foundation
- Data ingestion
- Baseline EDA
- Classification pipeline
- MLflow integration

### v0.2

- Survival Analysis
- Explainability (SHAP)

### v0.3

- Streamlit Dashboard

### v0.4

- AWS Deployment
- Pulumi Infrastructure

### v0.5

- Monitoring
- Drift Detection
- Automated Retraining

### v1.0

- Resume Intelligence
- Psychometric Intelligence
- Amazon Bedrock Integration
- Retention Advisor

## Author

- **Hubert Ronald** - Initial Work - [HubertRonald](https://github.com/HubertRonald)

## License

The source code in this repository is distributed under the MIT License. See
[LICENSE](./LICENSE) for more details.