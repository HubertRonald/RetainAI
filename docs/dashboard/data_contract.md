# Dashboard Data Contract

## Historical Dataset

Source:

```text
data/processed/ibm_hr_attrition_processed.csv
```

Required columns:

```text
Attrition
Department
JobRole
OverTime
BusinessTravel
MaritalStatus
EducationField
MonthlyIncome
TotalWorkingYears
YearsAtCompany
YearsInCurrentRole
YearsWithCurrManager
```

## Prediction Input

Input files must exclude `Attrition` and can be CSV or XLSX.

Sample files:

```text
data/prediction_input/ibm_hr_attrition_prediction_sample.csv
data/prediction_input/ibm_hr_attrition_prediction_sample.xlsx
```

## Prediction Output

```text
prediction
attrition_probability
risk_level
```

## Explainability Artifacts

```text
artifacts/reports/explainability_report.md
artifacts/reports/explainability_report_<model>.md
artifacts/figures/explainability/<model>/*.png
artifacts/explanations/<model>/metadata.json
```

## Survival Artifacts

```text
artifacts/reports/survival_report.md
artifacts/figures/survival/*.png
```
