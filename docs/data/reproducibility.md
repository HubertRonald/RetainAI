# Data Reproducibility

The data pipeline is designed to run without notebooks.

## Step 1 — Download raw dataset

```bash
python -m retainai.data.download_ibm_hr
Step 2 — Validate, clean and split dataset
python -m retainai.data.prepare_dataset
```

Expected outputs

```text
data/
├── processed/
│   └── ibm_hr_attrition_processed.csv
├── train/
│   └── ibm_hr_attrition_train.csv
├── validation/
│   └── ibm_hr_attrition_validation.csv
└── test/
    └── ibm_hr_attrition_test.csv
```

Pipeline flow:

```text
raw
 ↓
schema validation
 ↓
processed
 ↓
train / validation / test
```