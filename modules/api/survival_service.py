from pathlib import Path


def available_survival_figures(figures_dir: str | Path) -> list[str]:
    path = Path(figures_dir)
    return sorted([p.name for p in path.glob("*.png")]) if path.exists() else []
