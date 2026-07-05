# RetainAI EDA Summary

This report is generated from reusable EDA modules and is intended to support documentation, modeling decisions, dashboard design, and future monitoring workflows.


## Dataset Overview

| metric          |   value |
|:----------------|--------:|
| rows            |    1470 |
| columns         |      35 |
| duplicated_rows |       0 |


## Target Distribution

| target_value   |   count |   percentage |
|:---------------|--------:|-------------:|
| No             |    1233 |        83.88 |
| Yes            |     237 |        16.12 |


## Column Profile

| column                   | dtype   |   non_null_count |   null_count |   null_pct |   unique_count |
|:-------------------------|:--------|-----------------:|-------------:|-----------:|---------------:|
| Age                      | int64   |             1470 |            0 |          0 |             43 |
| Attrition                | object  |             1470 |            0 |          0 |              2 |
| BusinessTravel           | object  |             1470 |            0 |          0 |              3 |
| DailyRate                | int64   |             1470 |            0 |          0 |            886 |
| Department               | object  |             1470 |            0 |          0 |              3 |
| DistanceFromHome         | int64   |             1470 |            0 |          0 |             29 |
| Education                | int64   |             1470 |            0 |          0 |              5 |
| EducationField           | object  |             1470 |            0 |          0 |              6 |
| EmployeeCount            | int64   |             1470 |            0 |          0 |              1 |
| EmployeeNumber           | int64   |             1470 |            0 |          0 |           1470 |
| EnvironmentSatisfaction  | int64   |             1470 |            0 |          0 |              4 |
| Gender                   | object  |             1470 |            0 |          0 |              2 |
| HourlyRate               | int64   |             1470 |            0 |          0 |             71 |
| JobInvolvement           | int64   |             1470 |            0 |          0 |              4 |
| JobLevel                 | int64   |             1470 |            0 |          0 |              5 |
| JobRole                  | object  |             1470 |            0 |          0 |              9 |
| JobSatisfaction          | int64   |             1470 |            0 |          0 |              4 |
| MaritalStatus            | object  |             1470 |            0 |          0 |              3 |
| MonthlyIncome            | int64   |             1470 |            0 |          0 |           1349 |
| MonthlyRate              | int64   |             1470 |            0 |          0 |           1427 |
| NumCompaniesWorked       | int64   |             1470 |            0 |          0 |             10 |
| Over18                   | object  |             1470 |            0 |          0 |              1 |
| OverTime                 | object  |             1470 |            0 |          0 |              2 |
| PercentSalaryHike        | int64   |             1470 |            0 |          0 |             15 |
| PerformanceRating        | int64   |             1470 |            0 |          0 |              2 |
| RelationshipSatisfaction | int64   |             1470 |            0 |          0 |              4 |
| StandardHours            | int64   |             1470 |            0 |          0 |              1 |
| StockOptionLevel         | int64   |             1470 |            0 |          0 |              4 |
| TotalWorkingYears        | int64   |             1470 |            0 |          0 |             40 |
| TrainingTimesLastYear    | int64   |             1470 |            0 |          0 |              7 |
| WorkLifeBalance          | int64   |             1470 |            0 |          0 |              4 |
| YearsAtCompany           | int64   |             1470 |            0 |          0 |             37 |
| YearsInCurrentRole       | int64   |             1470 |            0 |          0 |             19 |
| YearsSinceLastPromotion  | int64   |             1470 |            0 |          0 |             16 |
| YearsWithCurrManager     | int64   |             1470 |            0 |          0 |             18 |


## Numeric Profile

| column                   |   count |         mean |         std |   min |     25% |     50% |      75% |   max |
|:-------------------------|--------:|-------------:|------------:|------:|--------:|--------:|---------:|------:|
| Age                      |    1470 |    36.9238   |    9.13537  |    18 |   30    |    36   |    43    |    60 |
| DailyRate                |    1470 |   802.486    |  403.509    |   102 |  465    |   802   |  1157    |  1499 |
| DistanceFromHome         |    1470 |     9.19252  |    8.10686  |     1 |    2    |     7   |    14    |    29 |
| Education                |    1470 |     2.91293  |    1.02416  |     1 |    2    |     3   |     4    |     5 |
| EmployeeCount            |    1470 |     1        |    0        |     1 |    1    |     1   |     1    |     1 |
| EmployeeNumber           |    1470 |  1024.87     |  602.024    |     1 |  491.25 |  1020.5 |  1555.75 |  2068 |
| EnvironmentSatisfaction  |    1470 |     2.72177  |    1.09308  |     1 |    2    |     3   |     4    |     4 |
| HourlyRate               |    1470 |    65.8912   |   20.3294   |    30 |   48    |    66   |    83.75 |   100 |
| JobInvolvement           |    1470 |     2.72993  |    0.711561 |     1 |    2    |     3   |     3    |     4 |
| JobLevel                 |    1470 |     2.06395  |    1.10694  |     1 |    1    |     2   |     3    |     5 |
| JobSatisfaction          |    1470 |     2.72857  |    1.10285  |     1 |    2    |     3   |     4    |     4 |
| MonthlyIncome            |    1470 |  6502.93     | 4707.96     |  1009 | 2911    |  4919   |  8379    | 19999 |
| MonthlyRate              |    1470 | 14313.1      | 7117.79     |  2094 | 8047    | 14235.5 | 20461.5  | 26999 |
| NumCompaniesWorked       |    1470 |     2.6932   |    2.49801  |     0 |    1    |     2   |     4    |     9 |
| PercentSalaryHike        |    1470 |    15.2095   |    3.65994  |    11 |   12    |    14   |    18    |    25 |
| PerformanceRating        |    1470 |     3.15374  |    0.360824 |     3 |    3    |     3   |     3    |     4 |
| RelationshipSatisfaction |    1470 |     2.71224  |    1.08121  |     1 |    2    |     3   |     4    |     4 |
| StandardHours            |    1470 |    80        |    0        |    80 |   80    |    80   |    80    |    80 |
| StockOptionLevel         |    1470 |     0.793878 |    0.852077 |     0 |    0    |     1   |     1    |     3 |
| TotalWorkingYears        |    1470 |    11.2796   |    7.78078  |     0 |    6    |    10   |    15    |    40 |
| TrainingTimesLastYear    |    1470 |     2.79932  |    1.28927  |     0 |    2    |     3   |     3    |     6 |
| WorkLifeBalance          |    1470 |     2.76122  |    0.706476 |     1 |    2    |     3   |     3    |     4 |
| YearsAtCompany           |    1470 |     7.00816  |    6.12653  |     0 |    3    |     5   |     9    |    40 |
| YearsInCurrentRole       |    1470 |     4.22925  |    3.62314  |     0 |    2    |     3   |     7    |    18 |
| YearsSinceLastPromotion  |    1470 |     2.18776  |    3.22243  |     0 |    0    |     1   |     3    |    15 |
| YearsWithCurrManager     |    1470 |     4.12313  |    3.56814  |     0 |    2    |     3   |     7    |    17 |


## Categorical Profile

| column         |   unique_count | top_value              |   top_frequency |
|:---------------|---------------:|:-----------------------|----------------:|
| Attrition      |              2 | No                     |            1233 |
| BusinessTravel |              3 | Travel_Rarely          |            1043 |
| Department     |              3 | Research & Development |             961 |
| EducationField |              6 | Life Sciences          |             606 |
| Gender         |              2 | Male                   |             882 |
| JobRole        |              9 | Sales Executive        |             326 |
| MaritalStatus  |              3 | Married                |             673 |
| Over18         |              1 | Y                      |            1470 |
| OverTime       |              2 | No                     |            1054 |


## Missing Data Summary

| column                   |   missing_count |   missing_pct |
|:-------------------------|----------------:|--------------:|
| Age                      |               0 |             0 |
| Attrition                |               0 |             0 |
| BusinessTravel           |               0 |             0 |
| DailyRate                |               0 |             0 |
| Department               |               0 |             0 |
| DistanceFromHome         |               0 |             0 |
| Education                |               0 |             0 |
| EducationField           |               0 |             0 |
| EmployeeCount            |               0 |             0 |
| EmployeeNumber           |               0 |             0 |
| EnvironmentSatisfaction  |               0 |             0 |
| Gender                   |               0 |             0 |
| HourlyRate               |               0 |             0 |
| JobInvolvement           |               0 |             0 |
| JobLevel                 |               0 |             0 |
| JobRole                  |               0 |             0 |
| JobSatisfaction          |               0 |             0 |
| MaritalStatus            |               0 |             0 |
| MonthlyIncome            |               0 |             0 |
| MonthlyRate              |               0 |             0 |
| NumCompaniesWorked       |               0 |             0 |
| Over18                   |               0 |             0 |
| OverTime                 |               0 |             0 |
| PercentSalaryHike        |               0 |             0 |
| PerformanceRating        |               0 |             0 |
| RelationshipSatisfaction |               0 |             0 |
| StandardHours            |               0 |             0 |
| StockOptionLevel         |               0 |             0 |
| TotalWorkingYears        |               0 |             0 |
| TrainingTimesLastYear    |               0 |             0 |
| WorkLifeBalance          |               0 |             0 |
| YearsAtCompany           |               0 |             0 |
| YearsInCurrentRole       |               0 |             0 |
| YearsSinceLastPromotion  |               0 |             0 |
| YearsWithCurrManager     |               0 |             0 |


## Constant Columns

- `EmployeeCount`
- `Over18`
- `StandardHours`


## High Cardinality Categorical Columns

_No rows to display._


## Attrition Rate by Department

| Department             |   attrition_rate_pct |   count |
|:-----------------------|---------------------:|--------:|
| Sales                  |              20.6278 |     446 |
| Human Resources        |              19.0476 |      63 |
| Research & Development |              13.8398 |     961 |


## Attrition Rate by JobRole

| JobRole                   |   attrition_rate_pct |   count |
|:--------------------------|---------------------:|--------:|
| Sales Representative      |             39.759   |      83 |
| Laboratory Technician     |             23.9382  |     259 |
| Human Resources           |             23.0769  |      52 |
| Sales Executive           |             17.4847  |     326 |
| Research Scientist        |             16.0959  |     292 |
| Manufacturing Director    |              6.89655 |     145 |
| Healthcare Representative |              6.87023 |     131 |
| Manager                   |              4.90196 |     102 |
| Research Director         |              2.5     |      80 |


## Attrition Rate by OverTime

| OverTime   |   attrition_rate_pct |   count |
|:-----------|---------------------:|--------:|
| Yes        |              30.5288 |     416 |
| No         |              10.4364 |    1054 |


## Attrition Rate by BusinessTravel

| BusinessTravel    |   attrition_rate_pct |   count |
|:------------------|---------------------:|--------:|
| Travel_Frequently |              24.9097 |     277 |
| Travel_Rarely     |              14.9569 |    1043 |
| Non-Travel        |               8      |     150 |


## Attrition Rate by MaritalStatus

| MaritalStatus   |   attrition_rate_pct |   count |
|:----------------|---------------------:|--------:|
| Single          |              25.5319 |     470 |
| Married         |              12.4814 |     673 |
| Divorced        |              10.0917 |     327 |


## Attrition Rate by Gender

| Gender   |   attrition_rate_pct |   count |
|:---------|---------------------:|--------:|
| Male     |              17.0068 |     882 |
| Female   |              14.7959 |     588 |


## Attrition Rate by MonthlyIncome Bins

| MonthlyIncome_bin   |   attrition_rate_pct |   count |
|:--------------------|---------------------:|--------:|
| (1008.999, 2695.8]  |             31.2925  |     294 |
| (2695.8, 4228.8]    |             17.0068  |     294 |
| (5743.4, 9860.0]    |             12.585   |     294 |
| (4228.8, 5743.4]    |             10.5442  |     294 |
| (9860.0, 19999.0]   |              9.18367 |     294 |


## Attrition Rate by Age Bins

| Age_bin        |   attrition_rate_pct |   count |
|:---------------|---------------------:|--------:|
| (17.999, 29.0] |             27.9141  |     326 |
| (29.0, 34.0]   |             18.1538  |     325 |
| (45.0, 60.0]   |             12.4542  |     273 |
| (38.0, 45.0]   |              9.96564 |     291 |
| (34.0, 38.0]   |              9.41176 |     255 |


## Attrition Rate by YearsAtCompany Bins

| YearsAtCompany_bin   |   attrition_rate_pct |   count |
|:---------------------|---------------------:|--------:|
| (-0.001, 2.0]        |             29.8246  |     342 |
| (2.0, 5.0]           |             13.8249  |     434 |
| (7.0, 10.0]          |             12.4113  |     282 |
| (5.0, 7.0]           |             12.0482  |     166 |
| (10.0, 40.0]         |              8.13008 |     246 |


## Attrition Rate by DistanceFromHome Bins

| DistanceFromHome_bin   |   attrition_rate_pct |   count |
|:-----------------------|---------------------:|--------:|
| (17.0, 29.0]           |              20.2166 |     277 |
| (9.0, 17.0]            |              18.9723 |     253 |
| (2.0, 5.0]             |              15.493  |     213 |
| (5.0, 9.0]             |              14.9351 |     308 |
| (0.999, 2.0]           |              12.8878 |     419 |


## Attrition Rate by TotalWorkingYears Bins

| TotalWorkingYears_bin   |   attrition_rate_pct |   count |
|:------------------------|---------------------:|--------:|
| (-0.001, 5.0]           |             28.7975  |     316 |
| (5.0, 8.0]              |             18.123   |     309 |
| (8.0, 10.0]             |             11.745   |     298 |
| (10.0, 17.0]            |             11.4943  |     261 |
| (17.0, 40.0]            |              8.74126 |     286 |


## Target Numeric Correlations

| feature                  |   correlation |
|:-------------------------|--------------:|
| TotalWorkingYears        |   -0.171063   |
| JobLevel                 |   -0.169105   |
| YearsInCurrentRole       |   -0.160545   |
| MonthlyIncome            |   -0.15984    |
| Age                      |   -0.159205   |
| YearsWithCurrManager     |   -0.156199   |
| StockOptionLevel         |   -0.137145   |
| YearsAtCompany           |   -0.134392   |
| JobInvolvement           |   -0.130016   |
| JobSatisfaction          |   -0.103481   |
| EnvironmentSatisfaction  |   -0.103369   |
| DistanceFromHome         |    0.0779236  |
| WorkLifeBalance          |   -0.063939   |
| TrainingTimesLastYear    |   -0.0594778  |
| DailyRate                |   -0.056652   |
| RelationshipSatisfaction |   -0.0458723  |
| NumCompaniesWorked       |    0.0434937  |
| YearsSinceLastPromotion  |   -0.0330188  |
| Education                |   -0.0313728  |
| MonthlyRate              |    0.0151702  |
| PercentSalaryHike        |   -0.0134782  |
| EmployeeNumber           |   -0.0105772  |
| HourlyRate               |   -0.00684555 |
| PerformanceRating        |    0.00288875 |
| EmployeeCount            |  nan          |
