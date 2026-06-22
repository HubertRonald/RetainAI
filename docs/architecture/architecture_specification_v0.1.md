# RetainAI

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
    <a href="https://pandas.pydata.org/" target="_blank">
        <img src="https://img.shields.io/badge/Pandas-DataFrames-150458?style=flat-square&logo=pandas&logoColor=white" />
    </a>
    <a href="https://numpy.org/" target="_blank">
        <img src="https://img.shields.io/badge/NumPy-Arrays-013243?style=flat-square&logo=numpy&logoColor=white" />
    </a>
    <a href="https://jupyter.org/" target="_blank">
        <img src="https://img.shields.io/badge/Jupyter-Notebooks-F37626?style=flat-square&logo=jupyter&logoColor=white" />
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
    <a href="https://www.docker.com/" target="_blank">
        <img src="https://img.shields.io/badge/Docker-Services-2496ED?style=flat-square&logo=docker&logoColor=white" />
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
    <img src="https://img.shields.io/github/last-commit/HubertRonald/RetainAI?style=flat-square" />
    <img src="https://img.shields.io/github/license/HubertRonald/RetainAI?style=flat-square&color=success" />
</p>


**AI-ready Employee Retention Intelligence Platform**

RetainAI is an AWS-native MLOps and analytics project for employee attrition and retention intelligence. It combines classical machine learning, survival analysis, explainability, dashboard analytics, and a future-ready AI roadmap for resume intelligence, psychometric analysis, RAG, and Amazon Bedrock integration.

## Project scope

RetainAI is designed as a portfolio-grade MLOps platform for employee retention analytics. The first version uses the public IBM HR Analytics Employee Attrition dataset from Kaggle as a reproducible benchmark.

The platform is planned around:

* attrition classification;
* survival analysis;
* explainability;
* Streamlit dashboard analytics;
* MLflow experiment tracking;
* AWS deployment;
* data drift and retraining workflows;
* future AI extensions with resumes, psychometric tests, RAG, and Amazon Bedrock.

## Data source

This repository does not redistribute the IBM HR Analytics dataset.

Users must download the dataset directly from Kaggle:

```bash
mkdir -p data/raw/ibm_hr_attrition

kaggle datasets download \
  -d pavansubhasht/ibm-hr-analytics-attrition-dataset \
  -p data/raw/ibm_hr_attrition \
  --unzip
```

Expected local layout:

```text
data/
└── raw/
    └── ibm_hr_attrition/
        └── WA_Fn-UseC_-HR-Employee-Attrition.csv
```

## Repository structure

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
├── README.md
└── LICENSE
```

## Architecture specification

The initial architecture specification is available at:

```text
docs/architecture/architecture_specification_v0.1.md
```

## License

This project is released under the MIT License. See
[LICENSE](../../LICENSE) for more details.