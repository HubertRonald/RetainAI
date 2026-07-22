"""Cross-cloud authentication and AI quota middleware."""

from __future__ import annotations

import hmac
import os
import time
from collections.abc import Iterable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp

from modules.security.usage_quota import UsageQuota, build_usage_quota_from_env


class SecurityQuotaMiddleware(BaseHTTPMiddleware):
    """Protect backend routes and enforce quota before AI provider calls."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.auth_enabled = _env_bool("RETAINAI_BACKEND_AUTH_ENABLED", True)
        self.backend_token = os.getenv("RETAINAI_BACKEND_TOKEN", "")
        self.quota_enabled = _env_bool("RETAINAI_QUOTA_ENABLED", True)
        self.ai_provider = os.getenv("RETAINAI_AI_PROVIDER", "disabled").lower()
        self.public_paths = _csv_set(
            os.getenv(
                "RETAINAI_PUBLIC_PATHS",
                "/health,/docs,/openapi.json,/redoc",
            )
        )
        self.ai_prefixes = tuple(
            _csv_values(
                os.getenv(
                    "RETAINAI_AI_ENDPOINT_PREFIXES",
                    "/advisor,/api/advisor,/ai,/rag",
                )
            )
        )
        self.quota: UsageQuota | None = None
        self.quota_error: str | None = None

        if self.quota_enabled:
            try:
                self.quota = build_usage_quota_from_env()
            except (RuntimeError, ValueError) as exc:
                self.quota_error = str(exc)

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        path = request.url.path

        if request.method == "OPTIONS" or path in self.public_paths:
            return await call_next(request)

        auth_response = self._validate_backend_token(request)
        if auth_response is not None:
            return auth_response

        if not self._is_ai_path(path):
            return await call_next(request)

        if self.ai_provider == "disabled":
            return JSONResponse(
                status_code=503,
                content={
                    "detail": "AI endpoints are disabled by configuration.",
                    "code": "ai_disabled",
                },
            )

        if not self.quota_enabled:
            return JSONResponse(
                status_code=503,
                content={
                    "detail": "AI quota enforcement is disabled.",
                    "code": "quota_disabled",
                },
            )

        if self.quota is None:
            return JSONResponse(
                status_code=503,
                content={
                    "detail": "AI quota backend is unavailable.",
                    "code": "quota_unavailable",
                },
            )

        client_identifier = _client_identifier(request)
        endpoint_group = _endpoint_group(path)
        decision = self.quota.consume(
            client_identifier=client_identifier,
            endpoint_group=endpoint_group,
            provider=self.ai_provider,
        )

        quota_headers = {
            "X-RateLimit-Limit": str(decision.limit),
            "X-RateLimit-Remaining": str(decision.remaining),
            "X-RateLimit-Reset": str(decision.reset_at),
        }

        if not decision.allowed:
            retry_after = max(decision.reset_at - int(time.time()), 1)
            return JSONResponse(
                status_code=429,
                headers={**quota_headers, "Retry-After": str(retry_after)},
                content={
                    "detail": "AI request quota exceeded.",
                    "code": "quota_exceeded",
                    "limit": decision.limit,
                    "reset_at": decision.reset_at,
                },
            )

        response = await call_next(request)
        response.headers.update(quota_headers)
        return response

    def _validate_backend_token(self, request: Request) -> JSONResponse | None:
        if not self.auth_enabled:
            return None

        if not self.backend_token:
            return JSONResponse(
                status_code=503,
                content={
                    "detail": "Backend authentication is enabled but not configured.",
                    "code": "auth_not_configured",
                },
            )

        supplied = _supplied_token(request)
        if not supplied or not hmac.compare_digest(supplied, self.backend_token):
            return JSONResponse(
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"},
                content={
                    "detail": "Invalid or missing backend token.",
                    "code": "unauthorized",
                },
            )

        return None

    def _is_ai_path(self, path: str) -> bool:
        return any(path == prefix or path.startswith(f"{prefix}/") for prefix in self.ai_prefixes)


def _supplied_token(request: Request) -> str | None:
    authorization = request.headers.get("authorization", "")
    scheme, _, value = authorization.partition(" ")
    if scheme.lower() == "bearer" and value.strip():
        return value.strip()

    legacy_header = request.headers.get("x-retainai-backend-token", "").strip()
    return legacy_header or None


def _client_identifier(request: Request) -> str:
    # Cloud Run should set a server-side pseudonymous identifier when available.
    for header_name in ("x-retainai-client-id", "x-retainai-client-ip"):
        value = request.headers.get(header_name, "").strip()
        if value:
            return value

    forwarded_for = request.headers.get("x-forwarded-for", "")
    if forwarded_for:
        first_hop = forwarded_for.split(",", maxsplit=1)[0].strip()
        if first_hop:
            return first_hop

    return request.client.host if request.client else "unknown"


def _endpoint_group(path: str) -> str:
    parts = [part for part in path.split("/") if part]
    return parts[0] if parts else "root"


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _csv_values(value: str) -> Iterable[str]:
    return (item.strip() for item in value.split(",") if item.strip())


def _csv_set(value: str) -> set[str]:
    return set(_csv_values(value))
