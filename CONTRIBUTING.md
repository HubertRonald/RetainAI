# Contributing to RetainAI

Thank you for your interest in contributing to RetainAI.

RetainAI is an experimental MLOps and employee retention intelligence platform focused on reproducibility, explainability, survival analysis, and AI-ready workforce analytics.

## Development Environment

The recommended development environment is:

* VS Code
* Dev Containers
* Python 3.10

After opening the project in the Dev Container:

```bash
pip install -e ".[dev,test]"
```

## Repository Philosophy

RetainAI follows a modular architecture:

```text
modules/   → reusable analytical components
src/       → application and product logic
notebooks/ → exploratory and research workflows
services/  → deployment and serving components
apps/      → user-facing applications
```

Notebook code should not become production code directly.

Reusable logic should be migrated into:

```text
modules/
src/retainai/
```

## Branching Strategy

Primary branches:

```text
main
feature/mlops-foundation
```

Development work should be performed on feature branches and merged into the active development branch before reaching main.

## Code Style

Formatting tools:

* black
* isort
* ruff

Run:

```bash
python -m tox -e lint
```

before opening a pull request.

## Testing

Unit tests:

```bash
python -m tox -e py310
```

Integration tests should be added when new services or workflows are introduced.

## Data Policy

The IBM HR Analytics dataset is not redistributed by this repository.

Users must download the dataset directly from Kaggle and comply with the dataset license and terms of use.

## Documentation

Repository-facing documentation must be written in English.

Documentation should prioritize:

* reproducibility
* methodological transparency
* architectural clarity

## Future Roadmap

RetainAI is expected to evolve toward:

* survival analysis
* explainability
* workforce intelligence
* resume intelligence
* psychometric intelligence
* Amazon Bedrock integration

Contributions aligned with these areas are especially welcome.
