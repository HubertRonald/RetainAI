from __future__ import annotations

import os
from typing import Any

import pandas as pd
import requests

DEFAULT_API_URL = os.getenv("RETAINAI_API_URL", "http://localhost:8001")


class RetainAIApiClient:
    def __init__(self, base_url: str | None = None, timeout: int = 30) -> None:
        self.base_url = (base_url or DEFAULT_API_URL).rstrip("/")
        self.timeout = timeout

    def health(self) -> dict[str, Any]:
        response = requests.get(f"{self.base_url}/health", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def predict(self, df: pd.DataFrame, model_name: str) -> pd.DataFrame:
        payload = {
            "model_name": model_name,
            "records": df.to_dict(orient="records"),
        }

        candidate_paths = [
            "/prediction/predict",
            "/predict",
            "/api/predict",
        ]

        last_error: Exception | None = None

        for path in candidate_paths:
            try:
                response = requests.post(
                    f"{self.base_url}{path}",
                    json=payload,
                    timeout=self.timeout,
                )
                if response.status_code == 404:
                    continue
                response.raise_for_status()
                data = response.json()
                return self._normalize_prediction_response(data=data, input_df=df)
            except Exception as exc:  # noqa: BLE001
                last_error = exc

        raise RuntimeError(
            "API prediction failed. Check available API routes and payload contract."
        ) from last_error

    @staticmethod
    def _normalize_prediction_response(
        data: dict[str, Any] | list[dict[str, Any]],
        input_df: pd.DataFrame,
    ) -> pd.DataFrame:
        if isinstance(data, list):
            return pd.DataFrame(data)

        if "predictions" in data:
            predictions = data["predictions"]
            if isinstance(predictions, list):
                output = input_df.copy()
                pred_df = pd.DataFrame(predictions)
                for col in pred_df.columns:
                    output[col] = pred_df[col].values
                return output

        if "records" in data:
            return pd.DataFrame(data["records"])

        output = input_df.copy()
        for key, value in data.items():
            if isinstance(value, list) and len(value) == len(output):
                output[key] = value

        return output
