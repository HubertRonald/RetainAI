# Explainability Report

Version: v0.2

Sprint: Sprint 5 — Explainability

---

## Executive Summary

The Explainability layer successfully generated reproducible SHAP explanations for all baseline predictive models implemented in RetainAI.

Supported models:

* Logistic Regression
* Random Forest
* XGBoost

Each model produced:

* global feature importance rankings;
* SHAP beeswarm visualization;
* representative local explanation;
* serialized SHAP artifacts;
* reusable metadata for downstream applications.

---

## Cross-model observations

Several predictors consistently appear among the most influential variables across different model families.

Frequently recurring features include:

* MonthlyIncome
* OverTime
* Age
* JobLevel
* TotalWorkingYears
* YearsWithCurrManager
* EnvironmentSatisfaction
* JobSatisfaction
* StockOptionLevel
* DistanceFromHome

These variables therefore represent robust candidate drivers of employee attrition regardless of model architecture.   

---

## Logistic Regression

The linear baseline produces explanations that are highly interpretable.

Important variables include:

* JobLevel
* MonthlyIncome
* TotalWorkingYears
* YearsSinceLastPromotion
* NumCompaniesWorked
* OverTime
* JobSatisfaction

These explanations align well with classical HR analytics literature and provide an interpretable reference model. 

---

## Random Forest

The Random Forest model distributes feature importance across a larger number of predictors.

Compared with Logistic Regression, the model assigns greater importance to:

* StockOptionLevel
* YearsAtCompany
* DailyRate
* HourlyRate

while still preserving the relevance of:

* MonthlyIncome
* Age
* OverTime. 

---

## XGBoost

XGBoost produced the strongest nonlinear explanation patterns.

The most influential variables include:

* OverTime
* StockOptionLevel
* MonthlyIncome
* Age
* NumCompaniesWorked
* YearsWithCurrManager

The prominence of interaction-driven variables suggests that gradient boosting captures more complex relationships than linear models while remaining explainable through SHAP. 

---

## Explainability Artifacts

The Explainability pipeline generates:

* SHAP values;
* expected values;
* feature importance tables;
* beeswarm plots;
* waterfall examples;
* reusable metadata.

These artifacts are stored independently of model training and can be reused without recomputing SHAP values.

---

## Future Integration

The Explainability artifacts constitute the foundation for subsequent RetainAI components.

Planned consumers include:

* Streamlit Dashboard;
* Monitoring layer;
* Drift Detection;
* Retention Advisor;
* Amazon Bedrock integration.

---

## Conclusion

It establishes a fully reproducible explainability workflow that transforms predictive models into transparent analytical assets.

The resulting artifacts are suitable for dashboard visualization, model auditing, AI-assisted recommendation systems, and future enterprise deployment.
