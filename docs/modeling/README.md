# Modeling

## Table of contents

- [Product objective](#product-objective)
- [Prediction boundary](#prediction-boundary)
- [Evaluation](#evaluation)
- [Explainability](#explainability)
- [Resume Intelligence](#resume-intelligence)
- [Retention Advisor](#retention-advisor)
- [Limitations](#limitations)
- [Related guides](#related-guides)

## Product objective

Models support identification and explanation of retention risk while preserving
human review.

## Prediction boundary

Every model must define:

```text
population
prediction target
time horizon
feature cutoff
exclusion criteria
decision context
```

## Evaluation

Evaluation should include:

```text
discrimination
calibration
precision and recall
threshold behavior
temporal validation
subgroup analysis
business interpretation
```

No single metric should define readiness.

## Explainability

Outputs should include structured evidence:

```text
risk score
important signals
confidence or uncertainty
data limitations
recommended next review
```

## Resume Intelligence

Resume Intelligence may provide structured context extraction and transparent
signals. It must not infer unsupported personality or psychometric traits.

## Retention Advisor

The advisor combines validated signals, evidence, policy, and optional provider
output into reviewable recommendations.

The advisor is decision support, not an autonomous employment decision-maker.

## Limitations

Psychometric Intelligence is outside v1.0 until supported by appropriate data,
validated instruments, fairness analysis, privacy review, and responsible
interpretation.

## Related guides

- [Data](../data/README.md)
- [MLOps](../mlops/README.md)
- [Prompts](../prompts/README.md)
- [Documentation index](../README.md)
