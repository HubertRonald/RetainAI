# Explainability Report

Model explained: `logistic_regression`

## Global SHAP Feature Importance

| feature                                       |   mean_abs_shap |
|:----------------------------------------------|----------------:|
| numeric__JobLevel                             |        0.549735 |
| numeric__MonthlyIncome                        |        0.471733 |
| numeric__TotalWorkingYears                    |        0.424355 |
| numeric__YearsSinceLastPromotion              |        0.423696 |
| numeric__NumCompaniesWorked                   |        0.405947 |
| categorical__OverTime_No                      |        0.359265 |
| numeric__JobSatisfaction                      |        0.346377 |
| numeric__EnvironmentSatisfaction              |        0.337649 |
| categorical__OverTime_Yes                     |        0.306879 |
| numeric__RelationshipSatisfaction             |        0.293467 |
| numeric__YearsWithCurrManager                 |        0.283127 |
| numeric__YearsInCurrentRole                   |        0.277629 |
| categorical__BusinessTravel_Travel_Frequently |        0.253191 |
| categorical__JobRole_Laboratory Technician    |        0.249432 |
| numeric__DistanceFromHome                     |        0.231682 |
| numeric__Age                                  |        0.231313 |
| categorical__MaritalStatus_Single             |        0.230747 |
| categorical__MaritalStatus_Divorced           |        0.203018 |
| numeric__JobInvolvement                       |        0.202091 |
| numeric__TrainingTimesLastYear                |        0.196138 |
| categorical__BusinessTravel_Non-Travel        |        0.175278 |
| categorical__JobRole_Sales Representative     |        0.173284 |
| numeric__StockOptionLevel                     |        0.171638 |
| numeric__WorkLifeBalance                      |        0.154537 |
| numeric__PercentSalaryHike                    |        0.152525 |

## Notes

- SHAP values explain feature contributions to model predictions.
- Global importance is computed as mean absolute SHAP value.
- Local explanations are generated for representative validation samples.