from __future__ import annotations

from modules.eda.report import generate_eda_summary
from modules.io.datasets import load_ibm_hr_dataset
from retainai.core.paths import PROJECT_ROOT


def main() -> None:
    df = load_ibm_hr_dataset()
    output_path = PROJECT_ROOT / "artifacts" / "reports" / "eda_summary.md"

    report_path = generate_eda_summary(df=df, output_path=output_path)

    print(f"EDA summary generated at: {report_path}")


if __name__ == "__main__":
    main()
