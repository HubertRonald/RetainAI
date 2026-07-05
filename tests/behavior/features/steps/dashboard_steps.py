from pathlib import Path

from behave import given, then


@given("the dashboard planning documents exist")
def step_dashboard_docs_exist(context):
    context.architecture = Path("docs/architecture/dashboard_architecture.md")
    context.layout = Path("docs/dashboard/layout_specification.md")
    assert context.architecture.exists()
    assert context.layout.exists()


@then("the dashboard architecture should define four analytical pages")
def step_dashboard_architecture_pages(context):
    text = context.architecture.read_text(encoding="utf-8")
    for page in [
        "Executive Overview",
        "Prediction Center",
        "Explainability Explorer",
        "Survival Analytics",
    ]:
        assert page in text


@given("the dashboard service contract exists")
def step_service_contract_exists(context):
    context.service_contract = Path("docs/dashboard/service_contract.md")
    assert context.service_contract.exists()


@then("the API domains should include overview, predict, explainability and survival")
def step_api_domains_exist(context):
    text = context.service_contract.read_text(encoding="utf-8")
    for domain in ["overview", "predict", "explainability", "survival"]:
        assert f"/api/v1/{domain}" in text


@given("the dashboard mockup specification exists")
def step_mockup_spec_exists(context):
    context.mockup = Path("docs/dashboard/mockup_specification.md")
    assert context.mockup.exists()


@then("it should include the fancy dark layout contract")
def step_mockup_dark_layout(context):
    text = context.mockup.read_text(encoding="utf-8").lower()
    for token in ["dark", "sidebar", "kpi", "status", "runtime"]:
        assert token in text
