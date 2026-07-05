# Missing Data Analysis

RetainAI includes a formal missing data analysis layer.

The first public IBM HR dataset is expected to contain no missing values. However, the missing data analysis layer is retained because future enterprise HR datasets may contain incomplete fields such as compensation, psychometric scores, resume-derived features or onboarding indicators.

The missing data workflow covers:

- missing value summary;
- missing value percentage by feature;
- shadow matrix generation;
- missingness correlation;
- future imputation strategy.

Missing data mechanisms considered:

- MCAR: Missing Completely At Random;
- MAR: Missing At Random;
- MNAR: Missing Not At Random.

Initial imputation is intentionally not performed during EDA. Imputation belongs to the feature engineering and preprocessing pipeline.