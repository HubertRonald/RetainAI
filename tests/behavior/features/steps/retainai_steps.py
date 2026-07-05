from __future__ import annotations

import pandas as pd
from behave import given, then, when

from modules.classification.preprocessing import build_feature_target
from modules.eda.quality import target_distribution
from modules.preprocessing.validation import validate_schema


@given("a synthetic HR dataset")
def step_synthetic_hr_dataset(context):
    context.df = pd.DataFrame(
        {
            "Age": [25, 35, 45, 29],
            "Attrition": ["Yes", "No", "No", "Yes"],
            "OverTime": ["Yes", "No", "No", "Yes"],
            "YearsAtCompany": [1, 5, 12, 2],
        }
    )


@when("the dataset schema is validated")
def step_validate_schema(context):
    schema = {
        "dataset": "behavior_hr",
        "target": "Attrition",
        "target_values": ["Yes", "No"],
        "required_columns": ["Age", "Attrition", "OverTime", "YearsAtCompany"],
    }
    context.report = validate_schema(context.df, schema)


@then("the validation report should be valid")
def step_report_valid(context):
    assert context.report.is_valid is True


@when("the attrition distribution is computed")
def step_compute_distribution(context):
    context.distribution = target_distribution(context.df)


@then("both attrition classes should be present")
def step_classes_present(context):
    assert set(context.distribution["target_value"]) == {"Yes", "No"}


@when("classification features are built")
def step_build_features(context):
    context.X, context.y = build_feature_target(context.df)


@then("the target should be binary encoded")
def step_target_binary(context):
    assert set(context.y.unique()) == {0, 1}
