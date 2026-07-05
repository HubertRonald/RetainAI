# Data Quality

The data quality layer evaluates whether the dataset is suitable for modeling and dashboard analytics.

Current checks include:

- duplicated rows;
- constant columns;
- high-cardinality categorical features;
- target class distribution;
- schema consistency.

Constant features in the IBM HR dataset, such as `EmployeeCount`, `Over18`, or `StandardHours`, may be candidates for removal during feature engineering.

Data quality checks are separated from modeling to support future MLOps validation and drift monitoring workflows.