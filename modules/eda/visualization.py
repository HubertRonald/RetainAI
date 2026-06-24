from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('seaborn-v0_8')
plt.rcParams.update({"legend.frameon": True})


def plot_target_distribution(
        df: pd.DataFrame,
        target: str = "Attrition",
    ) -> None:
    counts = df[target].value_counts()

    fig, ax = plt.subplots(figsize=(6, 4))
    counts.plot(kind="bar", ax=ax)
    ax.set_title(f"{target} Distribution")
    ax.set_xlabel(target)
    ax.set_ylabel("Count")
    plt.tight_layout()


def plot_attrition_by_category(
        df: pd.DataFrame,
        column: str,
        target: str = "Attrition",
    ) -> None:
    crosstab = pd.crosstab(df[column], df[target], normalize="index") * 100

    fig, ax = plt.subplots(figsize=(8, 4))
    crosstab.plot(kind="bar", ax=ax)
    ax.set_title(f"{target} by {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Percentage")
    plt.tight_layout()


def plot_correlation_heatmap(corr: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(10, 8))
    image = ax.imshow(corr, aspect="auto")
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=90)
    ax.set_yticks(range(len(corr.index)))
    ax.set_yticklabels(corr.index)
    fig.colorbar(image, ax=ax)
    ax.set_title("Numeric Correlation Matrix")
    plt.tight_layout()
