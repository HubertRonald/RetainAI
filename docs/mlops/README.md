# MLOps

## Table of contents

- [Purpose](#purpose)
- [Model lifecycle](#model-lifecycle)
- [Monitoring](#monitoring)
- [Drift detection](#drift-detection)
- [Validation reports](#validation-reports)
- [Retraining governance](#retraining-governance)
- [Release and rollback](#release-and-rollback)
- [Related guides](#related-guides)

## Purpose

MLOps provides repeatable evaluation, monitoring, release, and governance for
RetainAI analytical capabilities.

## Model lifecycle

```text
data version
training
evaluation
approval
registration
deployment
monitoring
review
retirement
```

## Monitoring

v0.5 should establish:

```text
data quality monitoring
prediction distribution monitoring
model-performance monitoring
service health
quota and error visibility
```

## Drift detection

Distinguish:

```text
input drift
prediction drift
target drift
performance degradation
concept drift
```

A drift alert is evidence for investigation, not automatic proof that a model
must be replaced.

## Validation reports

Dashboard reports should summarize:

```text
dataset version
model version
evaluation window
quality checks
performance metrics
drift status
known limitations
```

## Retraining governance

Automated retraining requires:

```text
versioned datasets
reproducible pipelines
approval gates
evaluation thresholds
model registry
rollback
audit trail
```

Retraining should not deploy automatically solely because drift was detected.

## Release and rollback

Application deployment and infrastructure deployment remain separate.

Every release should have an immutable identifier and a documented rollback
path.

## Related guides

- [Data](../data/README.md)
- [Modeling](../modeling/README.md)
- [Multicloud](../multicloud/README.md)
- [Documentation index](../README.md)
