from __future__ import annotations

from pathlib import Path

import pandas as pd

from modules.eda.attrition import (
    attrition_rate_by_category,
    attrition_rate_by_numeric_bins,
)
from modules.eda.correlations import target_numeric_correlation
from modules.eda.missingness import missing_summary
from modules.eda.profiling import (
    categorical_profile,
    column_profile,
    dataset_overview,
    numeric_profile,
)
from modules.eda.quality import (
    constant_columns,
    high_cardinality_columns,
    target_distribution,
)


def _markdown_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    table = df.copy()

    if max_rows is not None:
        table = table.head(max_rows)

    if table.empty:
        return "_No rows to display._"

    return table.to_markdown(index=False)


def _section(title: str, body: str) -> str:
    return f"\n## {title}\n\n{body}\n"


def generate_eda_summary(
    df: pd.DataFrame,
    output_path: str | Path = "artifacts/reports/eda_summary.md",
    target: str = "Attrition",
) -> Path:
    """Generate a markdown EDA summary artifact.

    This artifact is intended to capture reproducible evidence from notebooks
    and reusable EDA modules. It should feed `docs/eda/findings.md`, which is
    reserved for interpreted findings and narrative conclusions.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    sections: list[str] = [
        "# RetainAI EDA Summary\n",
        (
            "This report is generated from reusable EDA modules and is intended "
            "to support documentation, modeling decisions, dashboard design, "
            "and future monitoring workflows.\n"
        ),
    ]

    sections.append(_section("Dataset Overview", _markdown_table(dataset_overview(df))))
    sections.append(
        _section(
            "Target Distribution",
            _markdown_table(target_distribution(df, target=target)),
        )
    )
    sections.append(
        _section("Column Profile", _markdown_table(column_profile(df), max_rows=40))
    )
    sections.append(
        _section("Numeric Profile", _markdown_table(numeric_profile(df), max_rows=40))
    )
    sections.append(
        _section(
            "Categorical Profile", _markdown_table(categorical_profile(df), max_rows=40)
        )
    )
    sections.append(
        _section(
            "Missing Data Summary", _markdown_table(missing_summary(df), max_rows=40)
        )
    )

    constants = constant_columns(df)
    constant_body = (
        "\n".join(f"- `{column}`" for column in constants)
        if constants
        else "_No constant columns detected._"
    )
    sections.append(_section("Constant Columns", constant_body))

    sections.append(
        _section(
            "High Cardinality Categorical Columns",
            _markdown_table(high_cardinality_columns(df)),
        )
    )

    for column in [
        "Department",
        "JobRole",
        "OverTime",
        "BusinessTravel",
        "MaritalStatus",
        "Gender",
    ]:
        if column in df.columns:
            sections.append(
                _section(
                    f"Attrition Rate by {column}",
                    _markdown_table(
                        attrition_rate_by_category(df, column=column, target=target),
                        max_rows=20,
                    ),
                )
            )

    for column in [
        "MonthlyIncome",
        "Age",
        "YearsAtCompany",
        "DistanceFromHome",
        "TotalWorkingYears",
    ]:
        if column in df.columns:
            sections.append(
                _section(
                    f"Attrition Rate by {column} Bins",
                    _markdown_table(
                        attrition_rate_by_numeric_bins(
                            df, column=column, target=target
                        ),
                        max_rows=20,
                    ),
                )
            )

    sections.append(
        _section(
            "Target Numeric Correlations",
            _markdown_table(target_numeric_correlation(df, target=target), max_rows=25),
        )
    )

    path.write_text("\n".join(sections), encoding="utf-8")
    return path
