from __future__ import annotations

from modules.dashboard.validation import validate_required_files
from retainai.core.paths import PROJECT_ROOT

REQUIRED_FILES = [
    "docs/architecture/dashboard_architecture.md",
    "docs/dashboard/layout_specification.md",
    "docs/dashboard/data_contract.md",
    "docs/dashboard/service_contract.md",
    "docs/dashboard/mockup_specification.md",
    "docs/dashboard/mockup_validation.md",
    "apps/dashboard/streamlit-app/.streamlit/config.toml",
    "services/compose.yaml",
]


def main() -> None:
    paths = [PROJECT_ROOT / item for item in REQUIRED_FILES]
    result = validate_required_files(paths)
    missing = [p for p, ok in result.items() if not ok]

    report_path = PROJECT_ROOT / "artifacts/reports/dashboard_validation.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Dashboard Validation Report", "", "## Required Files", ""]

    for path, exists in result.items():
        lines.append(f"- `{path}` — {'OK' if exists else 'MISSING'}")

    lines += [
        "",
        "## Status",
        "",
        "Ready for Streamlit implementation." if not missing else "Not ready yet.",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Dashboard validation report generated at: {report_path}")

    if missing:
        raise FileNotFoundError(missing)


if __name__ == "__main__":
    main()
