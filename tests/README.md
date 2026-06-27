# RetainAI Test Suite

This test suite validates the RetainAI foundation before moving into the dashboard sprint.

## Test types

### Unit tests

Located in:

```text
tests/unit/
```

They validate reusable logic in `modules/` and core package paths in `src/retainai/core`.

### Behavior tests

Located in:

```text
tests/behavior/features/
```

They use `behave` to validate high-level project behavior.

## Recommended execution

Inside the Dev Container:

```bash
python -m pip install -e ".[dev,test]"
python -m tox
```

Optional domains:

```bash
python -m tox -e survival
python -m tox -e explainability
python -m tox -e behavior
```

The tests use synthetic data and do not require the Kaggle dataset.

## Common fixes

### Format failures

If this command fails:

```bash
black --check src modules tests
```

run:

```bash
python -m tox -e format
```

or manually:

```bash
black src modules tests
isort src modules tests
ruff check src modules tests --fix
```

Then validate again:

```bash
python -m tox -e lint
```

### Stratified split failures with small fixtures

If a split test fails with:

```text
The least populated class in y has only 1 member
```

the test dataset is too small for stratified train / validation / test splitting.

Use a larger synthetic fixture with at least several samples per class after each split.

### Survival tests skipped

If survival tests are skipped because `lifelines` is missing, run:

```bash
python -m pip install -e ".[survival]"
python -m tox -e survival
```

### Explainability tests

For SHAP-related validation:

```bash
python -m pip install -e ".[explainability]"
python -m tox -e explainability
```

### Behavior tests

Behavior tests are executed with:

```bash
python -m tox -e behavior
```

### Full validation cycle

Recommended before opening a pull request:

```bash
python -m tox -e format
python -m tox
python -m tox -e behavior
```
