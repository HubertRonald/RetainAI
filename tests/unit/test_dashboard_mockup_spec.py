from pathlib import Path


def test_mockup_spec_contains_four_pages() -> None:
    text = Path("docs/dashboard/mockup_specification.md").read_text(encoding="utf-8")
    for page in [
        "Executive Overview",
        "Prediction Center",
        "Explainability Explorer",
        "Survival Analytics",
    ]:
        assert page in text


def test_mockup_spec_contains_runtime_modes() -> None:
    text = Path("docs/dashboard/mockup_specification.md").read_text(encoding="utf-8")
    for mode in ["local", "api", "s3", "aws"]:
        assert mode in text
