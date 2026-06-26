from __future__ import annotations

from pathlib import Path

import pandas as pd


def _markdown_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    table = df.copy()

    if max_rows is not None:
        table = table.head(max_rows)

    if table.empty:
        return "_No rows to display._"

    return table.to_markdown(index=False)


def generate_survival_report(
        survival_probabilities: pd.DataFrame,
        hazard_summary: pd.DataFrame,
        concordance_index: float,
        output_path: str | Path,
    ) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    content = [
        "# Survival Analysis Report",
        "",
        "This report summarizes the initial survival analysis layer for RetainAI.",
        "",
        "## Analytical Setup",
        "",
        "- Event: `Attrition = Yes`",
        "- Duration: `YearsAtCompany`",
        "- Censoring: `Attrition = No`",
        "",
        "## Kaplan-Meier Survival Probabilities",
        "",
        _markdown_table(survival_probabilities),
        "",
        "## Cox PH Concordance Index",
        "",
        f"`{concordance_index:.4f}`",
        "",
        "## Cox PH Hazard Ratios",
        "",
        _markdown_table(hazard_summary, max_rows=25),
        "",
        "## Notes",
        "",
        "- Kaplan-Meier provides a non-parametric survival curve.",
        "- Cox PH estimates covariate effects through hazard ratios.",
        "- Results are exploratory and depend on the proxy duration variable `YearsAtCompany`.",
    ]

    path.write_text("\n".join(content), encoding="utf-8")
    return path
