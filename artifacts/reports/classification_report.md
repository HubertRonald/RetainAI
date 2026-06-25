# Classification Report

This report summarizes baseline classification results for employee attrition prediction.

## Model Comparison

| model               |   accuracy |   precision |    recall |       f1 |   roc_auc |   pr_auc |
|:--------------------|-----------:|------------:|----------:|---------:|----------:|---------:|
| logistic_regression |   0.795455 |    0.410714 | 0.657143  | 0.505495 |  0.803552 | 0.57677  |
| xgboost             |   0.836364 |    0.454545 | 0.142857  | 0.217391 |  0.720772 | 0.404128 |
| random_forest       |   0.840909 |    0.5      | 0.0571429 | 0.102564 |  0.718687 | 0.35309  |

## Notes

- Accuracy is not the main metric because the target is imbalanced.
- PR AUC, recall and F1-score are especially relevant for attrition detection.
- Logistic Regression is used as the interpretable baseline.
- Random Forest and XGBoost are used as nonlinear tabular baselines.