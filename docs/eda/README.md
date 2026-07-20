# Exploratory Data Analysis

## Table of contents

- [Purpose](#purpose)
- [Workflow](#workflow)
- [Reproducibility](#reproducibility)
- [Core checks](#core-checks)
- [Reports](#reports)
- [Boundaries](#boundaries)
- [Related guides](#related-guides)

## Purpose

EDA characterizes the data before modeling and provides evidence for data
quality, feature design, and product interpretation.

## Workflow

```text
load versioned data
validate schema
profile distributions
inspect missingness
analyze temporal behavior
check target balance
study feature relationships
record findings
```

## Reproducibility

Notebooks should:

```text
use deterministic inputs
record dataset version
avoid hidden manual state
export reusable code where appropriate
separate exploration from production logic
```

## Core checks

```text
class balance
outliers
missingness
duplicates
temporal leakage
group representation
feature stability
unexpected proxies
```

## Reports

EDA outputs can support future dashboard validation reports, but exploratory
charts must not be presented as validated causal conclusions.

## Boundaries

EDA identifies patterns and hypotheses. It does not establish psychometric,
causal, or fairness validity by itself.

## Related guides

- [Data](../data/README.md)
- [Modeling](../modeling/README.md)
- [MLOps](../mlops/README.md)
- [Documentation index](../README.md)
