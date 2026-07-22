# Prompt Engineering

## Table of contents

- [Purpose](#purpose)
- [Prompt contract](#prompt-contract)
- [Structured output](#structured-output)
- [Evidence grounding](#evidence-grounding)
- [Provider abstraction](#provider-abstraction)
- [Localization](#localization)
- [Safety and review](#safety-and-review)
- [Versioning and evaluation](#versioning-and-evaluation)

## Purpose

Prompts translate structured RetainAI context into bounded, reviewable advisor
output.

## Prompt contract

Prompts should define:

```text
role
task
input schema
allowed evidence
output schema
failure behavior
safety constraints
locale
```

## Structured output

Prefer validated structured responses:

```json
{
  "recommendation_key": "advisor.action.review_manager_context",
  "rationale_keys": [],
  "evidence": [],
  "limitations": [],
  "confidence": null
}
```

## Evidence grounding

Provider output must reference supplied evidence and must not invent employee,
resume, psychometric, or organizational facts.

## Provider abstraction

Supported adapter states:

```text
disabled
gemini
bedrock
```

Prompt templates should not depend on a provider-specific response format.

## Localization

Prompt and explanation architecture must support:

```text
en
es
```

The backend should return stable message keys and variables where possible. The
dashboard renders localized text.

## Safety and review

Outputs remain advisory and reviewable. Prompts must not authorize autonomous
high-impact employment decisions.

## Versioning and evaluation

Track:

```text
prompt version
provider
model identifier
locale
input schema
output schema
evaluation dataset
quality results
```

## Related guides

- [Modeling](../modeling/README.md)
- [Dashboard](../dashboard/README.md)
- [Architecture](../architecture/README.md)
- [Documentation index](../README.md)
