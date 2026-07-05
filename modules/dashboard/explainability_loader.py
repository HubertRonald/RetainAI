from pathlib import Path


def list_explainability_models(base_dir: str | Path) -> list[str]:
    path = Path(base_dir)
    return (
        sorted([p.name for p in path.iterdir() if p.is_dir()]) if path.exists() else []
    )


def get_explainability_figures(
    figures_dir: str | Path, model_name: str
) -> dict[str, Path]:
    model_dir = Path(figures_dir) / model_name
    return {
        "feature_importance": model_dir / "feature_importance.png",
        "beeswarm": model_dir / "beeswarm.png",
        "waterfall": model_dir / "waterfall_example.png",
    }
