# Explainability Report

Model explained: `xgboost`

## Global SHAP Feature Importance

| feature                                        |   mean_abs_shap |
|:-----------------------------------------------|----------------:|
| categorical__OverTime_No                       |        0.648109 |
| numeric__StockOptionLevel                      |        0.476637 |
| numeric__MonthlyIncome                         |        0.435742 |
| numeric__Age                                   |        0.406575 |
| numeric__NumCompaniesWorked                    |        0.341085 |
| numeric__YearsWithCurrManager                  |        0.337918 |
| numeric__EnvironmentSatisfaction               |        0.299383 |
| numeric__RelationshipSatisfaction              |        0.291014 |
| numeric__DistanceFromHome                      |        0.275919 |
| numeric__JobSatisfaction                       |        0.261066 |
| numeric__WorkLifeBalance                       |        0.217149 |
| numeric__DailyRate                             |        0.211032 |
| categorical__BusinessTravel_Travel_Frequently  |        0.208189 |
| numeric__YearsSinceLastPromotion               |        0.20361  |
| categorical__JobRole_Research Scientist        |        0.20019  |
| numeric__HourlyRate                            |        0.158579 |
| numeric__JobInvolvement                        |        0.143332 |
| numeric__TotalWorkingYears                     |        0.143067 |
| categorical__Department_Research & Development |        0.140875 |
| categorical__JobRole_Laboratory Technician     |        0.118529 |
| categorical__Gender_Female                     |        0.114629 |
| categorical__JobRole_Sales Executive           |        0.112518 |
| numeric__Education                             |        0.109931 |
| numeric__YearsAtCompany                        |        0.106411 |
| numeric__PercentSalaryHike                     |        0.104101 |

## Notes

- SHAP values explain feature contributions to model predictions.
- Global importance is computed as mean absolute SHAP value.
- Local explanations are generated for representative validation samples.