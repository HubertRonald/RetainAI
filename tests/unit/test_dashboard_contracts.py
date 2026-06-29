from pathlib import Path


def test_dashboard_contract_documents_exist() -> None:
    required_docs = [
        "docs/architecture/dashboard_architecture.md",
        "docs/dashboard/data_contract.md",
        "docs/dashboard/service_contract.md",
        "docs/dashboard/layout_specification.md",
        "docs/dashboard/mockup_specification.md",
        "docs/dashboard/mockup_validation.md",
    ]
    for doc in required_docs:
        assert Path(doc).exists(), f"Missing dashboard contract: {doc}"


def test_service_contract_mentions_api_domains() -> None:
    text = Path("docs/dashboard/service_contract.md").read_text(encoding="utf-8")
    for domain in ["overview", "predict", "explainability", "survival"]:
        assert f"/api/v1/{domain}" in text
