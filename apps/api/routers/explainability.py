from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/explainability", tags=["explainability"])

@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "explainability"}

@router.get("/models")
def models() -> dict:
    return {"models": ["logistic_regression", "random_forest", "xgboost"]}
