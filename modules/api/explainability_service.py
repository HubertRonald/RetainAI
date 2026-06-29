from pathlib import Path


def available_explainability_models(base_dir: str | Path) -> list[str]:
    path = Path(base_dir)
    return (
        sorted([p.name for p in path.iterdir() if p.is_dir()]) if path.exists() else []
    )
