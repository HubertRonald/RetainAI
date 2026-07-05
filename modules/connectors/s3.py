from __future__ import annotations


class S3Connector:
    def __init__(self, bucket: str | None = None) -> None:
        self.bucket = bucket

    def is_configured(self) -> bool:
        return self.bucket is not None
