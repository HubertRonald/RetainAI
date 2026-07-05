# EDA Findings

This document summarizes the main interpreted findings from the exploratory data analysis stage.

The evidence is generated from reusable EDA modules and stored locally in:

```text
artifacts/reports/eda_summary.md
```

The findings below should be interpreted as exploratory observations, not causal conclusions.

## 1. Dataset Readiness

The IBM HR Attrition dataset contains 1,470 rows and 35 columns.

No duplicated rows were detected. The target variable, `Attrition`, is highly imbalanced:

| Attrition | Count | Percentage |
| --------- | ----: | ---------: |
| No        | 1,233 |     83.88% |
| Yes       |   237 |     16.12% |

This confirms that employee attrition should be treated as an imbalanced classification problem. Accuracy alone should not be used as the main evaluation metric in later modeling stages.

Recommended downstream metrics include:

* ROC AUC;
* PR AUC;
* recall for the attrition class;
* precision for the attrition class;
* F1-score;
* top-k recall.

## 2. Missing Data

No missing values were detected across the 35 dataset columns.

This simplifies the initial modeling pipeline because no imputation is required for the current public benchmark dataset. However, the missing data analysis layer remains relevant for future production-oriented datasets, where missing values may appear in fields such as compensation, psychometric scores, resume-derived attributes or onboarding indicators.

For this reason, missing data handling should remain part of RetainAI's reusable data quality architecture.

## 3. Constant Columns

Three constant columns were detected:

* `EmployeeCount`
* `Over18`
* `StandardHours`

These variables do not provide predictive information because they contain no variation in the current dataset.

They should be removed during the feature engineering stage unless there is a specific documentation reason to keep them in profiling outputs.

## 4. High Cardinality

No high-cardinality categorical columns were detected using the current threshold.

This reduces the risk of sparse one-hot encoding issues in the first modeling iteration. Standard categorical encoding strategies should be sufficient for the initial classification baseline.

## 5. Attrition by Department

Attrition rates vary by department:

| Department             | Attrition Rate | Count |
| ---------------------- | -------------: | ----: |
| Sales                  |         20.63% |   446 |
| Human Resources        |         19.05% |    63 |
| Research & Development |         13.84% |   961 |

Sales and Human Resources show higher attrition rates than Research & Development.

This suggests that department-level segmentation may be relevant for the dashboard and for later feature engineering. However, the Human Resources department has a smaller sample size, so its attrition rate should be interpreted carefully.

## 6. Attrition by Job Role

Attrition varies strongly across job roles:

| Job Role                  | Attrition Rate | Count |
| ------------------------- | -------------: | ----: |
| Sales Representative      |         39.76% |    83 |
| Laboratory Technician     |         23.94% |   259 |
| Human Resources           |         23.08% |    52 |
| Sales Executive           |         17.48% |   326 |
| Research Scientist        |         16.10% |   292 |
| Manufacturing Director    |          6.90% |   145 |
| Healthcare Representative |          6.87% |   131 |
| Manager                   |          4.90% |   102 |
| Research Director         |          2.50% |    80 |

The highest attrition rate appears among Sales Representatives, followed by Laboratory Technicians and Human Resources roles.

This is an important exploratory signal for future modeling, dashboard segmentation and SHAP interpretation.

## 7. Attrition by OverTime

Overtime shows one of the clearest exploratory differences:

| OverTime | Attrition Rate | Count |
| -------- | -------------: | ----: |
| Yes      |         30.53% |   416 |
| No       |         10.44% | 1,054 |

Employees with overtime have almost three times the attrition rate of employees without overtime.

This variable should be treated as a strong candidate predictor in later classification, survival analysis and explainability stages.

## 8. Attrition by Business Travel

Attrition also varies by business travel frequency:

| Business Travel   | Attrition Rate | Count |
| ----------------- | -------------: | ----: |
| Travel Frequently |         24.91% |   277 |
| Travel Rarely     |         14.96% | 1,043 |
| Non-Travel        |          8.00% |   150 |

Employees who travel frequently show a higher attrition rate than employees who travel rarely or do not travel.

This suggests that travel burden may be associated with attrition risk and should be considered in feature engineering and dashboard analysis.

## 9. Attrition by Marital Status

Attrition varies by marital status:

| Marital Status | Attrition Rate | Count |
| -------------- | -------------: | ----: |
| Single         |         25.53% |   470 |
| Married        |         12.48% |   673 |
| Divorced       |         10.09% |   327 |

Single employees show a higher attrition rate than married or divorced employees.

This feature may capture career stage, personal mobility or other unobserved factors. It should be used carefully and interpreted as an association rather than a causal driver.

## 10. Attrition by Gender

Attrition rates by gender are relatively close:

| Gender | Attrition Rate | Count |
| ------ | -------------: | ----: |
| Male   |         17.01% |   882 |
| Female |         14.80% |   588 |

The observed difference is smaller than the differences seen in variables such as `OverTime`, `JobRole`, `BusinessTravel` and `MaritalStatus`.

Gender should not be emphasized as a primary attrition driver without further fairness and bias analysis.

## 11. Modeling Implications

The EDA suggests that the first modeling baseline should account for:

* class imbalance;
* categorical features such as `JobRole`, `Department`, `BusinessTravel`, `OverTime` and `MaritalStatus`;
* constant feature removal;
* robust train / validation / test splits;
* metrics beyond accuracy.

Important candidate variables for Sprint 3 include:

* `OverTime`;
* `JobRole`;
* `Department`;
* `BusinessTravel`;
* `MaritalStatus`;
* `MonthlyIncome`;
* `Age`;
* `YearsAtCompany`;
* `JobSatisfaction`;
* `WorkLifeBalance`.

## 12. Dashboard Implications

The dashboard should include business-facing cuts for:

* attrition by department;
* attrition by job role;
* attrition by overtime;
* attrition by travel frequency;
* attrition by marital status;
* target class imbalance;
* high-risk segments.

These views are useful not only for EDA, but also for later model monitoring and drift analysis.

## 13. Summary

The dataset is clean and ready for baseline modeling.

The strongest exploratory signals appear in:

* overtime;
* job role;
* business travel;
* department;
* marital status.
