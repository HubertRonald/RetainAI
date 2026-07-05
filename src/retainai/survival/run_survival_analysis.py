from __future__ import annotations

import joblib

from modules.io.storage import load_dataframe
from modules.survival.coxph import fit_cox_ph, hazard_ratio_summary
from modules.survival.kaplan_meier import (
    fit_kaplan_meier,
    fit_kaplan_meier_by_group,
    survival_probabilities,
)
from modules.survival.metrics import cox_concordance_index
from modules.survival.preprocessing import (
    prepare_cox_features,
    prepare_survival_dataset,
)
from modules.survival.report import generate_survival_report
from modules.survival.visualization import (
    save_group_kaplan_meier_plot,
    save_hazard_ratio_plot,
    save_kaplan_meier_plot,
)
from retainai.core.paths import PROJECT_ROOT


def main() -> None:
    processed_path = PROJECT_ROOT / "data/processed/ibm_hr_attrition_processed.csv"
    df = load_dataframe(processed_path)

    drop_columns = [
        "EmployeeNumber",
        "EmployeeCount",
        "Over18",
        "StandardHours",
    ]

    survival_df = prepare_survival_dataset(
        df,
        duration_col="YearsAtCompany",
        event_col="Attrition",
        positive_class="Yes",
        drop_columns=drop_columns,
    )

    kmf = fit_kaplan_meier(survival_df)
    survival_probs = survival_probabilities(kmf, times=[1, 2, 3, 5, 10])

    figures_dir = PROJECT_ROOT / "artifacts/figures/survival"
    reports_dir = PROJECT_ROOT / "artifacts/reports"
    models_dir = PROJECT_ROOT / "artifacts/models"

    figures_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    save_kaplan_meier_plot(
        kmf,
        figures_dir / "kaplan_meier_overall.png",
    )

    for group_col in ["OverTime", "Department", "JobRole"]:
        if group_col in survival_df.columns:
            group_models = fit_kaplan_meier_by_group(survival_df, group_col=group_col)
            save_group_kaplan_meier_plot(
                group_models,
                figures_dir / f"kaplan_meier_by_{group_col.lower()}.png",
                title=f"Kaplan-Meier Survival by {group_col}",
            )

    cox_df = prepare_cox_features(survival_df)
    cox_model = fit_cox_ph(cox_df)

    partial_hazard = cox_model.predict_partial_hazard(cox_df)
    cindex = cox_concordance_index(cox_df, partial_hazard)

    hazard_summary = hazard_ratio_summary(cox_model)

    save_hazard_ratio_plot(
        hazard_summary,
        figures_dir / "hazard_ratios.png",
    )

    joblib.dump(cox_model, models_dir / "coxph.pkl")

    report_path = generate_survival_report(
        survival_probabilities=survival_probs,
        hazard_summary=hazard_summary,
        concordance_index=cindex,
        output_path=reports_dir / "survival_report.md",
    )

    print(f"Survival report generated at: {report_path}")


if __name__ == "__main__":
    main()
