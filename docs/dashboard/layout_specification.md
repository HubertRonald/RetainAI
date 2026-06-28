# Dashboard Layout Specification

## Global Layout

```text
Sidebar: runtime selector, model selector, historical filters, artifact status
Main: header, status strip, page content
```

## Page 1 — Executive Overview

- KPI cards
- Attrition by Department
- Target Distribution
- Attrition by Job Role
- Attrition by OverTime
- Attrition by BusinessTravel
- Attrition by MaritalStatus
- Data preview

## Page 2 — Prediction Center

- Download template
- Upload CSV/XLSX
- Validation status
- Uploaded preview
- Run prediction
- Prediction KPIs
- Prediction results
- Download predictions

## Page 3 — Explainability Explorer

- Model selector
- Artifact availability
- Global SHAP feature importance
- SHAP beeswarm
- Local waterfall
- Top drivers
- Explainability report summary

## Page 4 — Survival Analytics

- Survival KPIs
- Kaplan-Meier overall
- Kaplan-Meier by OverTime
- Kaplan-Meier by Department
- Kaplan-Meier by JobRole
- Cox hazard ratios
- Survival report summary
