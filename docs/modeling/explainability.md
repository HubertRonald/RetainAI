# Explainability

This document summarizes the SHAP-based explainability layer in RetainAI.

Generated evidence is available in:

```text
artifacts/reports/explainability_report_<model>.md
artifacts/figures/explainability/<model>/
artifacts/explanations/<model>/
```

## Objective

The explainability layer helps interpret employee attrition predictions by identifying the variables that contribute most to model outputs.

## Supported Models

The initial SHAP layer supports:

* Logistic Regression
* Random Forest
* XGBoost

## Global Explanations

Global explanations summarize overall model behavior using mean absolute SHAP values.

## Local Explanations

Local explanations describe why a specific validation sample receives a given prediction.

## Dashboard Relevance

Explainability artifacts are designed to be consumed by the future Streamlit dashboard without recalculating SHAP values.

## Future AI Integration

Structured SHAP outputs may later support natural-language explanations through Amazon Bedrock and the Retention Advisor roadmap.
