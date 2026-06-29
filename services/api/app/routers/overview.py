from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/overview", tags=["overview"])

@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "overview"}

@router.get("/kpis")
def kpis() -> dict:
    return {"total_employees": 0, "attrition_count": 0, "non_attrition_count": 0, "attrition_rate": 0.0, "source": "placeholder"}
