# Dashboard Mockup Specification

## Global Layout

```text
RetainAI Dashboard

Sidebar:
    Runtime: local / api / s3 / aws
    Model: logistic_regression / random_forest / xgboost
    Filters: Department / JobRole / OverTime / BusinessTravel / MaritalStatus
    Status: processed data / prediction sample / model artifact / explainability artifacts / survival artifacts

Main:
    top header
    status strip
    page content
```

## Header

```text
Title: RetainAI
Subtitle: Employee Retention Intelligence Platform
Status chips: Runtime / Model / Data / API
```

## Pages

```text
Executive Overview:
    KPIs, Department, Target Distribution, JobRole, OverTime, BusinessTravel, MaritalStatus, Data Preview

Prediction Center:
    Template, Upload, Validation, Preview, Run Prediction, KPIs, Results, Download

Explainability Explorer:
    Model selector, Global SHAP, Beeswarm, Waterfall, Top Drivers, Report Summary

Survival Analytics:
    Survival KPIs, KM Overall, KM by OverTime, KM by Department, KM by JobRole, Cox Hazard Ratios
```

## Visual Tone

- dark background;
- subtle borders;
- glass-like cards;
- soft purple accent;
- low visual noise;
- consistent risk colors;
- no external font dependency at runtime.
