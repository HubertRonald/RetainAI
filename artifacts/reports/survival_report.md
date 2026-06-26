# Survival Analysis Report

This report summarizes the initial survival analysis layer for RetainAI.

## Analytical Setup

- Event: `Attrition = Yes`
- Duration: `YearsAtCompany`
- Censoring: `Attrition = No`

## Kaplan-Meier Survival Probabilities

|   time |   survival_probability |
|-------:|-----------------------:|
|      1 |               0.948192 |
|      2 |               0.927792 |
|      3 |               0.911342 |
|      5 |               0.872931 |
|     10 |               0.776815 |

## Cox PH Concordance Index

`0.9509`

## Cox PH Hazard Ratios

| feature                          |         coef |   exp(coef) |           p |   coef lower 95% |   coef upper 95% |
|:---------------------------------|-------------:|------------:|------------:|-----------------:|-----------------:|
| OverTime_Yes                     |  0.805381    |    2.23755  | 9.72625e-14 |      0.593345    |      1.01742     |
| JobRole_Sales Representative     |  0.64356     |    1.90324  | 0.00340736  |      0.212825    |      1.07429     |
| JobRole_Laboratory Technician    |  0.405126    |    1.49949  | 0.006439    |      0.113689    |      0.696563    |
| BusinessTravel_Travel_Frequently |  0.391966    |    1.47989  | 0.00661235  |      0.109084    |      0.674848    |
| MaritalStatus_Single             |  0.361498    |    1.43548  | 0.00453364  |      0.11188     |      0.611116    |
| EducationField_Technical Degree  |  0.254245    |    1.28949  | 0.154049    |     -0.0953554   |      0.603845    |
| JobRole_Human Resources          |  0.202666    |    1.22466  | 0.46429     |     -0.340129    |      0.745462    |
| EducationField_Marketing         |  0.17095     |    1.18643  | 0.339606    |     -0.179914    |      0.521814    |
| Gender_Male                      |  0.138594    |    1.14866  | 0.191231    |     -0.0692487   |      0.346437    |
| Department_Sales                 |  0.124824    |    1.13295  | 0.411612    |     -0.173145    |      0.422794    |
| NumCompaniesWorked               |  0.0929792   |    1.09744  | 1.06196e-05 |      0.051601    |      0.134357    |
| BusinessTravel_Travel_Rarely     |  0.0381318   |    1.03887  | 0.767287    |     -0.214422    |      0.290685    |
| PerformanceRating                |  0.0167442   |    1.01689  | 0.917941    |     -0.301791    |      0.335279    |
| DistanceFromHome                 |  0.0144417   |    1.01455  | 0.0205075   |      0.00222502  |      0.0266584   |
| MonthlyRate                      |  5.46144e-06 |    1.00001  | 0.449232    |     -8.68456e-06 |      1.96074e-05 |
| HourlyRate                       | -1.75724e-05 |    0.999982 | 0.994502    |     -0.00501546  |      0.00498032  |
| MonthlyIncome                    | -2.86165e-05 |    0.999971 | 0.0642935   |     -5.89317e-05 |      1.69869e-06 |
| DailyRate                        | -0.000155478 |    0.999845 | 0.223254    |     -0.000405683 |      9.47278e-05 |
| PercentSalaryHike                | -0.0014991   |    0.998502 | 0.925231    |     -0.0328076   |      0.0298094   |
| JobRole_Sales Executive          | -0.00189156  |    0.99811  | 0.990462    |     -0.312021    |      0.308238    |
| Education                        | -0.00471345  |    0.995298 | 0.92513     |     -0.10302     |      0.0935931   |
| YearsSinceLastPromotion          | -0.0107486   |    0.989309 | 0.563808    |     -0.0472473   |      0.0257501   |
| Age                              | -0.019131    |    0.981051 | 0.00353095  |     -0.0319841   |     -0.00627792  |
| TotalWorkingYears                | -0.0344682   |    0.966119 | 0.000203224 |     -0.0526531   |     -0.0162833   |
| JobRole_Research Scientist       | -0.0421153   |    0.958759 | 0.776411    |     -0.332766    |      0.248535    |

## Notes

- Kaplan-Meier provides a non-parametric survival curve.
- Cox PH estimates covariate effects through hazard ratios.
- Results are exploratory and depend on the proxy duration variable `YearsAtCompany`.