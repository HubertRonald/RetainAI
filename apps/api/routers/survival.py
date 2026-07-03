from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/survival", tags=["survival"])

@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "survival"}

@router.get("/figures")
def figures() -> dict:
    return {"figures": [], "source": "placeholder"}
