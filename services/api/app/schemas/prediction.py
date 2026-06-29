from __future__ import annotations

from pydantic import BaseModel

class PredictionRecordRequest(BaseModel):
    records: list[dict]

class PredictionResponse(BaseModel):
    predictions: list[int]
    probabilities: list[float]
    risk_levels: list[str]
