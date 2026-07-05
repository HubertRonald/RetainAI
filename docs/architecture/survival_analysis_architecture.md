# Survival Analysis Architecture

Version: v0.1

Status: Draft

---

# 1. Purpose

The Survival Analysis layer extends the employee attrition classification pipeline by estimating **when** an employee is expected to leave the organization rather than only predicting **whether** attrition will occur.

While the classification stage produces a probability of attrition, the survival analysis stage estimates the expected employee tenure and survival probability over time.

This analytical capability supports more proactive workforce planning and complements binary classification with time-aware decision intelligence.

---

# 2. Analytical Objective

Estimate the probability that an employee remains in the organization after a given amount of time.

The Survival Analysis module provides:

- survival probability;
- expected employee tenure;
- hazard estimation;
- comparison between employee groups;
- explanatory covariates affecting employee retention.

The survival outputs will later be integrated into:

- executive dashboards;
- explainability workflows;
- retention simulations;
- AI-assisted recommendations.

---

# 3. Event Definition

The event of interest is employee attrition.

Formally,

Event:

    Attrition = "Yes"

This represents an employee leaving the organization.

The event is assumed to occur only once for each employee.

---

# 4. Time Definition

The IBM HR dataset does not contain an explicit time-to-event variable.

Therefore, the initial implementation defines:

Time variable

    YearsAtCompany

This variable represents the observed employment duration for each employee.

Future enterprise implementations may replace this variable with more precise timestamps such as:

- hiring date;
- resignation date;
- contract termination date;
- last active date.

The architecture intentionally keeps the time definition configurable.

---

# 5. Censoring Definition

Employees that have not experienced attrition at the observation date are considered right-censored observations.

Formally,

Attrition = "No"

indicates:

- employee still active;
- event not yet observed;
- right-censored sample.

This allows the use of standard survival analysis techniques.

---

# 6. Initial Survival Models

RetainAI v0.2 includes two complementary survival models.

## Kaplan-Meier Estimator

Purpose

Estimate the non-parametric survival function.

Primary outputs

- survival curve
- median survival time
- survival probabilities
- confidence intervals

Use cases

- organizational overview
- department comparison
- overtime comparison
- job role comparison

---

## Cox Proportional Hazards Model

Purpose

Estimate the effect of explanatory variables on employee hazard.

Primary outputs

- hazard ratios
- coefficient significance
- confidence intervals
- survival prediction

Use cases

- explain risk factors
- quantify feature importance
- support HR decision making

---

# 7. Module Architecture

The Survival Analysis implementation follows the same modular philosophy adopted across RetainAI.

modules/

    survival/

        preprocessing.py

        kaplan_meier.py

        coxph.py

        metrics.py

        visualization.py

        report.py

Responsibilities

preprocessing.py

- prepare survival dataset
- encode event
- encode duration
- validation

kaplan_meier.py

- Kaplan-Meier estimator
- group comparisons
- survival probabilities

coxph.py

- Cox PH fitting
- proportional hazards model
- coefficient extraction

metrics.py

- concordance index
- likelihood statistics
- survival metrics

visualization.py

- Kaplan-Meier curves
- cumulative hazard
- survival comparison plots

report.py

- markdown report generation
- reusable reporting interface

---

# 8. Source Package

Reusable execution logic lives inside:

src/

    retainai/

        survival/

            run_survival_analysis.py

Responsibilities

- load processed datasets
- prepare survival inputs
- fit Kaplan-Meier
- fit Cox PH
- generate artifacts
- export documentation

This entry point mirrors the existing classification pipeline.

---

# 9. Generated Artifacts

Execution should automatically generate reproducible artifacts.

artifacts/

    reports/

        survival_report.md

    figures/

        kaplan_meier.png

        cumulative_hazard.png

        hazard_ratios.png

    models/

        coxph.pkl

These artifacts are generated and should not be manually edited.

---

# 10. Documentation

Human-readable interpretation belongs to:

docs/

    modeling/

        survival.md

Unlike generated reports, this document summarizes:

- analytical conclusions;
- interpretation;
- modeling implications;
- business impact;
- future improvements.

This follows the same philosophy established for:

- findings.md
- classification.md

---

# 11. Dashboard Integration

The Survival layer will feed the Streamlit dashboard with:

Executive Overview

- overall survival curve

Employee Explorer

- individual survival probability

Business Views

- department comparison
- job role comparison
- overtime comparison

Future versions may include interactive scenario simulations.

---

# 12. Explainability Integration

The Cox PH model naturally provides interpretable hazard ratios.

Future SHAP integration will complement:

Classification

↓

SHAP

Survival

↓

Hazard Ratios

Together these components provide both predictive and explanatory perspectives.

---

# 13. Future Extensions

The architecture intentionally remains extensible.

Possible future enhancements include:

- Random Survival Forests
- DeepSurv
- Time-dependent Cox models
- Recurrent survival models
- Competing risks
- Multi-state survival models

These capabilities are outside the current v0.2 scope.
