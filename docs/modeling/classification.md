# Classification Modeling

This document summarizes the first supervised classification baseline for employee attrition prediction in RetainAI.

The generated evidence for this stage is available in:

```text
artifacts/reports/classification_report.md
```

## Objective

The goal of the classification stage is to predict whether an employee is likely to leave the organization.

The target variable is:

```text
Attrition
```

The positive class is:

```text
Yes
```

## Modeling Context

The exploratory analysis showed that the target is imbalanced:

| Attrition | Count | Percentage |
| --------- | ----: | ---------: |
| No        | 1,233 |     83.88% |
| Yes       |   237 |     16.12% |

Because of this imbalance, accuracy is not sufficient to evaluate model quality. The classification pipeline prioritizes metrics that are more informative for attrition detection.

## Baseline Models

The first classification baseline includes:

* Logistic Regression
* Random Forest
* XGBoost

These models were selected because they provide a useful progression:

| Model               | Role                                     |
| ------------------- | ---------------------------------------- |
| Logistic Regression | Interpretable baseline                   |
| Random Forest       | Nonlinear ensemble baseline              |
| XGBoost             | Strong tabular machine learning baseline |

## Validation Results

| model               | accuracy | precision |   recall |       f1 |  roc_auc |   pr_auc |
| ------------------- | -------: | --------: | -------: | -------: | -------: | -------: |
| logistic_regression | 0.795455 |  0.410714 | 0.657143 | 0.505495 | 0.803552 | 0.576770 |
| xgboost             | 0.836364 |  0.454545 | 0.142857 | 0.217391 | 0.720772 | 0.404128 |
| random_forest       | 0.840909 |  0.500000 | 0.057143 | 0.102564 | 0.718687 | 0.353090 |

## Interpretation

Logistic Regression achieved the strongest baseline performance for the current validation split when evaluated using PR AUC, recall and F1-score.

Although Random Forest and XGBoost achieved slightly higher accuracy, they produced much lower recall for the attrition class. This means they missed a larger share of employees who actually left.

For the current RetainAI objective, detecting potential attrition cases is more important than maximizing overall accuracy. Therefore, Logistic Regression is the preferred initial baseline.

## Why Accuracy Is Not Enough

The dataset is imbalanced, with approximately 84% non-attrition cases and 16% attrition cases.

A model can achieve high accuracy by mostly predicting the majority class. For this reason, later modeling iterations should focus on:

* PR AUC
* recall
* precision
* F1-score
* threshold tuning
* top-k recall

## Modeling Implications

The first baseline suggests that class-sensitive modeling is necessary.

Recommended next steps:

* perform threshold tuning for Logistic Regression;
* compare class weighting strategies;
* evaluate calibrated probabilities;
* inspect feature importance and SHAP explanations;
* evaluate model stability across different train / validation splits;
* preserve Logistic Regression as the benchmark for future models.

## Current Baseline Decision

For the initial classification baseline, RetainAI should use:

```text
Logistic Regression
```

as the reference model.

Tree-based models remain useful for comparison, explainability experiments and future hyperparameter tuning.
