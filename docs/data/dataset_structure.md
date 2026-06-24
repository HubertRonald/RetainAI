# Dataset Structure

Expected local raw dataset layout:

```text
data/
└── raw/
    └── ibm_hr_attrition/
        └── WA_Fn-UseC_-HR-Employee-Attrition.csv
```

The dataset contract is defined in:

```text
configs/schema/ibm_hr_attrition.yaml
```

The target column is:

```text
Attrition
```

The expected target values are:

```text
Yes
No
```

The current schema separates:

- required columns;
- categorical columns;
- numeric columns;
- binary categorical values.