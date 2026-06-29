from pathlib import Path


def get_survival_figures(figures_dir: str | Path) -> dict[str, Path]:
    path = Path(figures_dir)
    return {
        "overall": path / "kaplan_meier_overall.png",
        "overtime": path / "kaplan_meier_by_overtime.png",
        "department": path / "kaplan_meier_by_department.png",
        "jobrole": path / "kaplan_meier_by_jobrole.png",
        "hazard_ratios": path / "hazard_ratios.png",
    }
