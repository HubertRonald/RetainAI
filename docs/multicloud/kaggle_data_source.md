# RetainAI Kaggle Data Source

> Sprint 7.1 — Kaggle source documentation and local seed contract.

## 1. Initial Dataset

```text
Dataset:
  IBM HR Analytics Employee Attrition & Performance

Source:
  Kaggle

Dataset slug:
  pavansubhasht/ibm-hr-analytics-attrition-dataset

Expected file:
  WA_Fn-UseC_-HR-Employee-Attrition.csv
```

The dataset is used as an initial reproducible public input, not as a committed repository asset.

## 2. Repository Policy

The dataset must not be committed to Git.

Do not commit:

```text
data/raw/ibm_hr_attrition/*.csv
~/.kaggle/kaggle.json
Kaggle API tokens
```

The repository should only include:

```text
download instructions
data contracts
schema expectations
processing code
tests using synthetic or tiny fixture data
```

## 3. Local Kaggle Credential

The Kaggle CLI expects credentials at:

```text
~/.kaggle/kaggle.json
```

Recommended permissions:

```bash
chmod 600 ~/.kaggle/kaggle.json
```

## 4. Local Download Command

```bash
mkdir -p data/raw/ibm_hr_attrition

kaggle datasets download \
  -d pavansubhasht/ibm-hr-analytics-attrition-dataset \
  -p data/raw/ibm_hr_attrition \
  --unzip
```

Validation:

```bash
test -f data/raw/ibm_hr_attrition/WA_Fn-UseC_-HR-Employee-Attrition.csv
```

## 5. Why Not Lambda Kaggle Download in Sprint 7

A Lambda-based Kaggle ingestion is possible later, but it is not the Sprint 7.1 MVP.

Reasons:

```text
Kaggle credentials would need to be stored in AWS.
Lambda packaging would need Kaggle client dependencies.
Dataset download and unzip can create timeout/package-size concerns.
The initial dataset is public, small and benchmark-oriented.
The local reproducible seed path is enough before cloud ETL exists.
```

Sprint 7.1 recommendation:

```text
local Kaggle download
  ↓
local processing
  ↓
manual S3 seed only after bucket exists
```
