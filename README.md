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
<img src="https://img.shields.io/badge/lifelines-Survival%20Analysis-4B8BBE?style=flat-square" />
</a>

<a href="https://shap.readthedocs.io/" target="_blank">
<img src="https://img.shields.io/badge/SHAP-Explainability-8A2BE2?style=flat-square" />
</a>

<a href="https://mlflow.org/" target="_blank">
<img src="https://img.shields.io/badge/MLflow-Experiment%20Tracking-0194E2?style=flat-square&logo=mlflow&logoColor=white" />
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
<img src="https://img.shields.io/badge/Pulumi-IaC-8A3391?style=flat-square&logo=pulumi&logoColor=white" />
</a>

<a href="https://github.com/features/actions" target="_blank">
<img src="https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?style=flat-square&logo=githubactions&logoColor=white" />
</a>

<a href="https://www.docker.com/" target="_blank">
<img src="https://img.shields.io/badge/Docker-Containers-2496ED?style=flat-square&logo=docker&logoColor=white" />
</a>

<img src="https://img.shields.io/github/license/HubertRonald/RetainAI?style=flat-square&color=success"/>

<img src="https://img.shields.io/badge/status-active-success?style=flat-square"/>

</p>

# RetainAI

> Decision Intelligence Platform for Employee Retention

RetainAI is an end-to-end Machine Learning and MLOps platform for employee retention analytics.

Rather than providing only employee attrition prediction, RetainAI combines predictive modeling, survival analysis, explainable AI, reproducible experimentation, and future AI-assisted decision support into a modular analytics platform for Human Resources.

---

# Project Vision

RetainAI is designed as a Decision Intelligence System for Human Resources.

The long-term objective is to evolve from traditional employee attrition prediction toward an explainable AI platform capable of supporting workforce planning, retention strategies, and HR decision making.

The architecture is intentionally designed to evolve toward Amazon Bedrock-powered assistants without requiring major repository redesign.

---

# Current Capabilities

✔ Employee Attrition Classification

✔ Survival Analysis

✔ Explainable AI (SHAP)

✔ Experiment-ready MLflow architecture

✔ Reproducible Data Pipeline

✔ Modular preprocessing pipeline

✔ Notebook-driven research workflow

✔ Production-oriented package architecture

✔ AWS-ready deployment architecture

---

# Analytical Pipeline

```text
Kaggle Dataset
        │
        ▼
Dataset Acquisition
        │
        ▼
Validation
        │
        ▼
Preprocessing
        │
        ▼
EDA
        │
        ▼
Classification
        │
        ▼
Survival Analysis
        │
        ▼
Explainability
        │
        ▼
Dashboard
        │
        ▼
Future AI Components
```

---

# Repository Architecture

```text
RetainAI/

├── configs/
├── data/
├── docs/
├── modules/
├── notebooks/
├── artifacts/
├── figures/
├── requirements/
├── src/
├── tests/
└── .devcontainer/
```

The repository follows a layered architecture.

- **modules/** contains reusable analytical logic.
- **src/** contains production pipelines.
- **notebooks/** remain declarative and consume reusable modules.
- **artifacts/** stores reproducible analytical outputs.
- **docs/** contains architectural and methodological documentation.

---

# Public Dataset

RetainAI uses the IBM HR Analytics Employee Attrition dataset as an initial benchmark.

The dataset is **not redistributed** by this repository.

Expected directory structure:

```text
data/
└── raw/
    └── ibm_hr_attrition/
        └── WA_Fn-UseC_-HR-Employee-Attrition.csv
```

Dataset download:

```bash
python -m retainai.data.download_ibm_hr
```

or manually:

```bash
kaggle datasets download \
-d pavansubhasht/ibm-hr-analytics-attrition-dataset \
-p data/raw/ibm_hr_attrition \
--unzip
```

---

# Development Environment

Recommended environment:

- Python 3.10
- VS Code
- Dev Containers
- Docker

The development container provides a reproducible Linux environment independent of the host operating system, avoiding common dependency issues on macOS and Windows.

---

# Project Status

Current development branch:

```text
feature/mlops-foundation
```

Completed milestones:

## v0.1

- Repository Foundation
- Data Foundation
- Exploratory Data Analysis
- Classification Pipeline
- MLflow-ready Architecture

## v0.2

- Survival Analysis
- Explainability (SHAP)

---

# Roadmap

## v0.3

- Streamlit Dashboard
- Executive Analytics
- Individual Employee Prediction
- Batch Prediction

## v0.4

- AWS Deployment
- Pulumi Infrastructure
- FastAPI Production Services

## v0.5

- Model Monitoring
- Drift Detection
- Automated Retraining

## v1.0

- Resume Intelligence
- Psychometric Intelligence
- Amazon Bedrock Integration
- Retention Advisor

---

# Documentation

Architecture specifications are available under:

```text
docs/architecture/
```

Methodology documentation:

```text
docs/modeling/
```

Analytical documentation:

```text
docs/eda/
```

---

# Config

```bash
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel

# python -m pip uninstall -y shap numba llvmlite pyarrow cryptography

python -m pip install --no-cache-dir --only-binary=:all: \
  "llvmlite==0.43.0" \
  "numba==0.60.0" \
  "pyarrow==14.0.2" \
  "cryptography==45.0.7"

python -m pip install -e ".[all]"
```

---

## Author

- **Hubert Ronald** - Initial Work - [HubertRonald](https://github.com/HubertRonald)

## License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more details.