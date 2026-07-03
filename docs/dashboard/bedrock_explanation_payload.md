# Bedrock-ready Explanation Payload

## Purpose

The explanation payload is a structured JSON document designed to be consumed by a future Amazon Bedrock-based Retention Advisor.

Currently it does not call Bedrock.

## Payload Sections

```text
payload_type
payload_version
generated_at
model
prediction
employee_record
top_drivers
intended_use
```

## Intended Use

The payload can support future natural-language retention explanations, but should not be used as an automated HR decision system.

## Current Generation Point

The payload is generated in:

```text
apps/dashboard/streamlit-app/pages/02_prediction_center.py
```

after a user:

```text
uploads data -> runs prediction -> selects a row -> generates row-level explanation
```
