# Data

## Table of contents

- [Purpose](#purpose)
- [Data contracts](#data-contracts)
- [Schema and validation](#schema-and-validation)
- [Artifacts](#artifacts)
- [Lineage](#lineage)
- [Versioning](#versioning)
- [Privacy and governance](#privacy-and-governance)
- [Related guides](#related-guides)

## Purpose

The data layer provides reproducible, validated inputs for retention analysis,
modeling, monitoring, and dashboard evidence.

## Data contracts

Each dataset should document:

```text
source
grain
primary identifiers
target definition
feature window
observation window
allowed nullability
expected types
refresh behavior
```

## Schema and validation

Validation should cover:

```text
required columns
types
ranges
category domains
duplicate keys
missingness
temporal consistency
target leakage
```

## Artifacts

Versioned analytical artifacts should be reproducible from code and source data.

Avoid committing sensitive raw data.

## Lineage

Every dashboard result should be traceable to:

```text
dataset version
transformation
model version
evaluation version
explanation evidence
```

## Versioning

Use immutable dataset and artifact identifiers whenever practical.

Monitoring and retraining workflows must know which data version produced a
model or report.

## Privacy and governance

Retention data may involve high-impact employment context. Apply data
minimization, access control, appropriate retention periods, and human review.

## Related guides

- [EDA](../eda/README.md)
- [Modeling](../modeling/README.md)
- [MLOps](../mlops/README.md)
- [Documentation index](../README.md)
