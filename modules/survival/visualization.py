from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from lifelines import KaplanMeierFitter

plt.style.use("seaborn-v0_8")
plt.rcParams.update({"legend.frameon": True})


def save_kaplan_meier_plot(
    kmf: KaplanMeierFitter,
    output_path: str | Path,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    ax = kmf.plot_survival_function()
    ax.set_title("Kaplan-Meier Survival Curve")
    ax.set_xlabel("Years at Company")
    ax.set_ylabel("Survival Probability")

    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()

    return path


def save_group_kaplan_meier_plot(
    models: dict[str, KaplanMeierFitter],
    output_path: str | Path,
    title: str,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    for _, kmf in models.items():
        kmf.plot_survival_function(ax=ax)

    ax.set_title(title)
    ax.set_xlabel("Years at Company")
    ax.set_ylabel("Survival Probability")

    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()

    return path


def save_hazard_ratio_plot(
    hazard_summary: pd.DataFrame,
    output_path: str | Path,
    top_n: int = 15,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    plot_df = hazard_summary.head(top_n).copy()
    plot_df = plot_df.sort_values("exp(coef)", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(plot_df["feature"], plot_df["exp(coef)"])
    ax.axvline(1.0, linestyle="--")
    ax.set_title("Top Hazard Ratios")
    ax.set_xlabel("Hazard Ratio")

    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()

    return path
