# Survival Analysis

This document summarizes the survival analysis layer in RetainAI.

Generated evidence is available in:

```text
artifacts/reports/survival_report.md
```

## Analytical Objective

The survival analysis layer estimates how employee retention changes over time.

Unlike binary classification, which predicts whether attrition may occur, survival analysis estimates when attrition may occur and how retention probability evolves.

## Event Definition

The event of interest is:

```text
Attrition = Yes
```

## Duration Definition

The initial duration proxy is:

```text
YearsAtCompany
```

This is a proxy because the public IBM HR dataset does not include explicit hire and termination dates.

## Censoring Definition

Employees with:

```text
Attrition = No
```

are treated as right-censored observations.

## Models

Initial survival models:

* Kaplan-Meier estimator
* Cox Proportional Hazards model

## Interpretation

Kaplan-Meier provides a non-parametric view of employee survival probability.

Cox PH provides hazard ratios that help interpret which employee attributes are associated with higher or lower attrition hazard.

## Limitations

The survival analysis layer depends on the available public dataset structure.

Because the dataset does not include exact event timestamps, `YearsAtCompany` is used as the initial duration proxy.

Future enterprise implementations should use exact employment dates where available.
