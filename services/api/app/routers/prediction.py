from __future__ import annotations

from fastapi import APIRouter
from modules.api.prediction_service import assign_risk_level
from services.api.app.schemas.prediction import PredictionRecordRequest

router = APIRouter(prefix="/api/v1/predict", tags=["prediction"])

@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "prediction"}

@router.get("/template")
def template() -> dict:
    return {"status": "ok", "message": "Prediction template endpoint placeholder."}

@router.post("/records")
def predict_records(payload: PredictionRecordRequest) -> dict:
    n = len(payload.records)
    probabilities = [0.0 for _ in range(n)]
    return {"predictions": [0 for _ in range(n)], "probabilities": probabilities, "risk_levels": [assign_risk_level(p) for p in probabilities], "source": "placeholder"}
