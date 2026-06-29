from __future__ import annotations

from fastapi import FastAPI
from services.api.app.routers import explainability, overview, prediction, survival

app = FastAPI(title="RetainAI API", description="API service for RetainAI dashboard.", version="0.1.0")

@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "retainai-api"}

app.include_router(overview.router)
app.include_router(prediction.router)
app.include_router(explainability.router)
app.include_router(survival.router)
