# Retention Advisor Prompt Template

## Purpose

This template prepares structured RetainAI explanation payloads for a future Amazon Bedrock-based Retention Advisor.

## Responsible-use Constraints

The advisor must:

- avoid automated employment decisions;
- avoid protected-class assumptions;
- avoid unsupported psychological claims;
- explain risk as decision support, not as certainty;
- provide practical HR discussion points.

## Prompt Outputs

```text
1. Risk summary.
2. Top drivers in plain language.
3. Possible retention actions.
4. Caveats and responsible-use notes.
```

## Generation Point

Prompt previews are generated in:

```text
apps/dashboard/streamlit-app/pages/02_prediction_center.py
```
