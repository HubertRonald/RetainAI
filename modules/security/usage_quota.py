"""Usage quota backends for RetainAI AI-backed endpoints.

The production backend uses a DynamoDB conditional update so concurrent
requests cannot increment past the configured limit. Client identifiers are
hashed before they are used in table keys; raw IP addresses are not persisted.
"""

from __future__ import annotations

import hashlib
import os
import threading
import time
from dataclasses import dataclass
from typing import Any, Protocol

import boto3
from botocore.exceptions import ClientError


@dataclass(frozen=True)
class QuotaDecision:
    """Result of consuming one request from a fixed quota window."""

    allowed: bool
    limit: int
    remaining: int
    request_count: int
    window_start: int
    reset_at: int
    quota_key: str


class UsageQuota(Protocol):
    """Contract implemented by quota backends."""

    def consume(
        self,
        client_identifier: str,
        endpoint_group: str,
        provider: str = "ai",
    ) -> QuotaDecision:
        """Consume one request and return the resulting decision."""


class InMemoryUsageQuota:
    """Process-local quota backend for tests and local development only."""

    def __init__(self, limit: int = 3, window_seconds: int = 86_400) -> None:
        self.limit = _positive_int(limit, "limit")
        self.window_seconds = _positive_int(window_seconds, "window_seconds")
        self._counts: dict[str, int] = {}
        self._lock = threading.Lock()

    def consume(
        self,
        client_identifier: str,
        endpoint_group: str,
        provider: str = "ai",
    ) -> QuotaDecision:
        window_start, reset_at = _window_bounds(self.window_seconds)
        quota_key = _quota_key(
            client_identifier=client_identifier,
            endpoint_group=endpoint_group,
            provider=provider,
            window_start=window_start,
        )

        with self._lock:
            current = self._counts.get(quota_key, 0)
            if current >= self.limit:
                return _decision(
                    allowed=False,
                    count=current,
                    limit=self.limit,
                    window_start=window_start,
                    reset_at=reset_at,
                    quota_key=quota_key,
                )

            current += 1
            self._counts[quota_key] = current

        return _decision(
            allowed=True,
            count=current,
            limit=self.limit,
            window_start=window_start,
            reset_at=reset_at,
            quota_key=quota_key,
        )


class DynamoDBUsageQuota:
    """Concurrency-safe fixed-window quota backed by Amazon DynamoDB."""

    def __init__(
        self,
        table_name: str,
        limit: int = 3,
        window_seconds: int = 86_400,
        region_name: str | None = None,
        table: Any | None = None,
    ) -> None:
        if not table_name.strip():
            raise ValueError("table_name must not be empty")

        self.table_name = table_name
        self.limit = _positive_int(limit, "limit")
        self.window_seconds = _positive_int(window_seconds, "window_seconds")
        self._table = table or boto3.resource(
            "dynamodb",
            region_name=region_name,
        ).Table(table_name)

    def consume(
        self,
        client_identifier: str,
        endpoint_group: str,
        provider: str = "ai",
    ) -> QuotaDecision:
        window_start, reset_at = _window_bounds(self.window_seconds)
        quota_key = _quota_key(
            client_identifier=client_identifier,
            endpoint_group=endpoint_group,
            provider=provider,
            window_start=window_start,
        )
        client_hash = _sha256(client_identifier)
        expires_at = reset_at + self.window_seconds

        try:
            response = self._table.update_item(
                Key={"quota_key": quota_key},
                UpdateExpression=(
                    "SET request_count = if_not_exists(request_count, :zero) + :one, "
                    "quota_limit = :limit, "
                    "window_start = if_not_exists(window_start, :window_start), "
                    "reset_at = if_not_exists(reset_at, :reset_at), "
                    "expires_at = if_not_exists(expires_at, :expires_at), "
                    "client_hash = if_not_exists(client_hash, :client_hash), "
                    "endpoint_group = if_not_exists(endpoint_group, :endpoint_group), "
                    "provider = if_not_exists(provider, :provider)"
                ),
                ConditionExpression=(
                    "attribute_not_exists(request_count) OR request_count < :limit"
                ),
                ExpressionAttributeValues={
                    ":zero": 0,
                    ":one": 1,
                    ":limit": self.limit,
                    ":window_start": window_start,
                    ":reset_at": reset_at,
                    ":expires_at": expires_at,
                    ":client_hash": client_hash,
                    ":endpoint_group": endpoint_group,
                    ":provider": provider,
                },
                ReturnValues="ALL_NEW",
            )
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code")
            if error_code != "ConditionalCheckFailedException":
                raise

            item = self._table.get_item(
                Key={"quota_key": quota_key},
                ConsistentRead=True,
            ).get("Item", {})
            count = int(item.get("request_count", self.limit))
            return _decision(
                allowed=False,
                count=count,
                limit=self.limit,
                window_start=window_start,
                reset_at=reset_at,
                quota_key=quota_key,
            )

        count = int(response["Attributes"]["request_count"])
        return _decision(
            allowed=True,
            count=count,
            limit=self.limit,
            window_start=window_start,
            reset_at=reset_at,
            quota_key=quota_key,
        )


def build_usage_quota_from_env() -> UsageQuota:
    """Build the configured quota backend from environment variables."""

    backend = os.getenv("RETAINAI_QUOTA_BACKEND", "dynamodb").strip().lower()
    limit = int(os.getenv("RETAINAI_QUOTA_LIMIT", "3"))
    window_seconds = int(os.getenv("RETAINAI_QUOTA_WINDOW_SECONDS", "86400"))

    if backend == "memory":
        return InMemoryUsageQuota(limit=limit, window_seconds=window_seconds)

    if backend != "dynamodb":
        raise ValueError(f"Unsupported RETAINAI_QUOTA_BACKEND: {backend}")

    table_name = os.getenv("RETAINAI_QUOTA_TABLE", "").strip()
    if not table_name:
        raise RuntimeError(
            "RETAINAI_QUOTA_TABLE is required when RETAINAI_QUOTA_BACKEND=dynamodb"
        )

    return DynamoDBUsageQuota(
        table_name=table_name,
        limit=limit,
        window_seconds=window_seconds,
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
    )


def _window_bounds(window_seconds: int, now: int | None = None) -> tuple[int, int]:
    current = int(time.time()) if now is None else int(now)
    window_start = current - (current % window_seconds)
    return window_start, window_start + window_seconds


def _quota_key(
    client_identifier: str,
    endpoint_group: str,
    provider: str,
    window_start: int,
) -> str:
    normalized_client = client_identifier.strip() or "unknown"
    payload = "|".join(
        [normalized_client, provider.strip(), endpoint_group.strip(), str(window_start)]
    )
    return _sha256(payload)


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _decision(
    *,
    allowed: bool,
    count: int,
    limit: int,
    window_start: int,
    reset_at: int,
    quota_key: str,
) -> QuotaDecision:
    return QuotaDecision(
        allowed=allowed,
        limit=limit,
        remaining=max(limit - count, 0),
        request_count=count,
        window_start=window_start,
        reset_at=reset_at,
        quota_key=quota_key,
    )


def _positive_int(value: int, name: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return parsed
