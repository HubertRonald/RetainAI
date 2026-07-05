# Explainability Report

Model explained: `random_forest`

## Global SHAP Feature Importance

| feature                              |   mean_abs_shap |
|:-------------------------------------|----------------:|
| numeric__MonthlyIncome               |      0.0436395  |
| numeric__Age                         |      0.0361074  |
| categorical__OverTime_No             |      0.0349845  |
| numeric__StockOptionLevel            |      0.0341481  |
| categorical__OverTime_Yes            |      0.0323281  |
| numeric__YearsAtCompany              |      0.0289546  |
| numeric__YearsWithCurrManager        |      0.026743   |
| numeric__TotalWorkingYears           |      0.024671   |
| numeric__NumCompaniesWorked          |      0.0221327  |
| numeric__EnvironmentSatisfaction     |      0.0189485  |
| numeric__DistanceFromHome            |      0.0176427  |
| numeric__DailyRate                   |      0.0169811  |
| numeric__HourlyRate                  |      0.0167365  |
| numeric__JobLevel                    |      0.0148483  |
| numeric__MonthlyRate                 |      0.013781   |
| categorical__MaritalStatus_Single    |      0.0134189  |
| numeric__YearsInCurrentRole          |      0.0132743  |
| numeric__JobSatisfaction             |      0.0127182  |
| numeric__RelationshipSatisfaction    |      0.0121162  |
| numeric__PercentSalaryHike           |      0.0115106  |
| numeric__WorkLifeBalance             |      0.0106025  |
| categorical__Department_Sales        |      0.0100086  |
| numeric__YearsSinceLastPromotion     |      0.00986592 |
| categorical__JobRole_Sales Executive |      0.00930991 |
| numeric__JobInvolvement              |      0.00902062 |

## Notes

- SHAP values explain feature contributions to model predictions.
- Global importance is computed as mean absolute SHAP value.
- Local explanations are generated for representative validation samples.