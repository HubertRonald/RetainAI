# 1. Purpose

The Explainability layer complements predictive modeling by providing interpretable explanations of employee attrition predictions.

Rather than replacing predictive models, explainability helps analysts and HR professionals understand which factors contribute to individual and global attrition risk.

The Explainability module is designed to support transparent, reproducible and auditable AI-assisted decision making.

---

# 2. Analytical Objective

Estimate and communicate why a model predicts employee attrition.

The Explainability layer provides:

* global feature importance;
* local prediction explanations;
* feature contribution analysis;
* model comparison;
* explanation artifacts;
* dashboard-ready visualizations.

---

# 3. Initial Explainability Strategy

RetainAI v0.2 focuses on SHAP.

Supported models:

```text
Logistic Regression

Random Forest

XGBoost
```

Each model receives its own SHAP explainer.

---

# 4. Global Explainability

Purpose

Understand overall model behavior.

Outputs

* SHAP Feature Importance
* Mean Absolute SHAP Values
* Feature Ranking

Questions answered

Which variables are generally the most influential?

---

# 5. Local Explainability

Purpose

Explain a single employee prediction.

Outputs

* SHAP Waterfall Plot
* SHAP Force Plot
* Local Feature Contributions

Questions answered

Why was this employee predicted as high risk?

---

# 6. Model Comparison

Explainability should support multiple models.

```text
Logistic Regression

↓

LinearExplainer

----------------

Random Forest

↓

TreeExplainer

----------------

XGBoost

↓

TreeExplainer
```

The architecture abstracts the explainer selection.

---

# 7. Module Architecture

```
modules/

    explainability/

        preprocessing.py

        explainers.py

        shap_values.py

        feature_importance.py

        visualization.py

        report.py
```

---

## preprocessing.py

Responsibilities

* prepare inference matrix

* preserve feature names

* validate input consistency

---

## explainers.py

Factory responsible for selecting the correct SHAP explainer.

Example

```text
Logistic Regression

↓

LinearExplainer

Random Forest

↓

TreeExplainer

XGBoost

↓

TreeExplainer
```

No notebook should instantiate SHAP directly.

---

## shap_values.py

Responsibilities

* compute SHAP values

* cache explanations

* normalize outputs

---

## feature_importance.py

Responsibilities

* mean absolute SHAP

* ranking

* comparison

---

## visualization.py

Responsibilities

Generate:

* beeswarm plot

* waterfall plot

* dependence plot

* bar plot

* summary plot

---

## report.py

Generate

```text
artifacts/reports/explainability_report.md
```

---

# 8. Source Package

```
src/

    retainai/

        explainability/

            run_explainability.py
```

Responsibilities

* load trained models

* load validation data

* compute explanations

* export figures

* export markdown report

---

# 9. Generated Artifacts

```
artifacts/

    reports/

        explainability_report.md

    figures/

        explainability/

            feature_importance.png

            beeswarm.png

            summary_plot.png

            waterfall_example.png

            dependence_plot.png

    explanations/

        shap_values.joblib
```

---


# Explainability Architecture

Version: v0.1

Status: Draft

## 1. Purpose

The Explainability layer complements predictive modeling by providing interpretable explanations of employee attrition predictions.

## 2. Analytical Objective

Explain why a model predicts employee attrition using global and local explanation artifacts.

## 3. Initial Strategy

RetainAI v0.2 uses SHAP to explain:

- Logistic Regression
- Random Forest
- XGBoost

## 4. Module Architecture

```text
modules/explainability/
├── preprocessing.py
├── explainers.py
├── shap_values.py
├── feature_importance.py
├── visualization.py
└── report.py
```

## 5. Source Package

```text
src/retainai/explainability/run_explainability.py
```

## 6. Generated Artifacts

```text
artifacts/reports/explainability_report.md
artifacts/figures/explainability/
artifacts/explanations/
```

## 7. Notebook

```text
notebooks/06_explainability.ipynb
```

## 8. Dashboard Integration

The dashboard should consume generated explainability artifacts without recalculating SHAP values.