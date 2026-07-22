"""AWS Lambda adapter for the RetainAI FastAPI backend.

Sprint 7.5 scope:
- Adapt the existing FastAPI app to AWS Lambda with Mangum.
- Add a lightweight backend-token guard for non-health endpoints.
- Keep /health public so Cloud Run, API Gateway and operators can validate the backend.
"""

from __future__ import annotations

import os
from collections.abc import Iterable
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from mangum import Mangum

from apps.api.main import app


def _bool_env(name: str, default: bool = True) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _csv_env(name: str, default: Iterable[str]) -> set[str]:
    value = os.getenv(name)
    if value is None:
        return set(default)
    return {item.strip() for item in value.split(",") if item.strip()}


def _has_route(path: str) -> bool:
    return any(getattr(route, "path", None) == path for route in app.routes)


def _extract_backend_token(request: Request) -> str | None:
    bearer = request.headers.get("authorization")
    if bearer and bearer.lower().startswith("bearer "):
        return bearer.split(" ", 1)[1].strip()

    token = request.headers.get("x-retainai-backend-token")
    if token:
        return token.strip()

    return None


DEFAULT_AUTH_EXEMPT_PATHS = {
    "/health",
    "/openapi.json",
}


if not _has_route("/health"):

    @app.get("/health", tags=["system"])
    def health() -> dict[str, Any]:
        """Public health endpoint for Lambda/API Gateway checks."""
        return {
            "status": "ok",
            "service": "retainai-api",
            "runtime": "aws-lambda",
        }


@app.middleware("http")
async def require_backend_token(request: Request, call_next):  # type: ignore[no-untyped-def]
    """Require a shared backend token for protected Lambda/API Gateway endpoints.

    Local override:
      RETAINAI_BACKEND_AUTH_ENABLED=false

    Protected mode:
      RETAINAI_BACKEND_AUTH_ENABLED=true
      RETAINAI_BACKEND_TOKEN=<secret>
      header: Authorization: Bearer <secret>
      or:     x-retainai-backend-token: <secret>
    """
    if not _bool_env("RETAINAI_BACKEND_AUTH_ENABLED", default=True):
        return await call_next(request)

    exempt_paths = _csv_env("RETAINAI_AUTH_EXEMPT_PATHS", DEFAULT_AUTH_EXEMPT_PATHS)

    if request.url.path in exempt_paths:
        return await call_next(request)

    expected_token = os.getenv("RETAINAI_BACKEND_TOKEN")

    if not expected_token:
        return JSONResponse(
            status_code=503,
            content={
                "detail": "Backend token auth is enabled but RETAINAI_BACKEND_TOKEN is not configured."
            },
        )

    provided_token = _extract_backend_token(request)

    if provided_token != expected_token:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid or missing backend token."},
        )

    return await call_next(request)


handler = Mangum(app, lifespan="auto")
