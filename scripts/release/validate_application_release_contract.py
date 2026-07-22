#!/usr/bin/env python3
"""Validate the RetainAI manual application-release contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


WORKFLOW = Path(
    ".github/workflows/multicloud-application-release.yml"
)

FORBIDDEN_WORKFLOW_TOKENS = (
    "terraform apply",
    "terraform destroy",
    "aws s3 ",
    "gcloud storage ",
    "pulumi ",
)

REQUIRED_WORKFLOW_SNIPPETS = (
    "workflow_dispatch:",
    'if [[ "${GITHUB_REF_NAME}" != "main" ]]',
    "scripts/release/detect_application_changes.sh",
    "google-github-actions/auth@v3",
    "aws-actions/configure-aws-credentials@v6.1.2",
    "gcloud run services update",
    "aws lambda update-function-code",
    "deploy-dashboard-${RELEASE_ENVIRONMENT}-${SHORT_SHA}",
    "deploy-backend-${RELEASE_ENVIRONMENT}-${SHORT_SHA}",
)

AUTOMATIC_TRIGGERS = (
    re.compile(r"(?m)^\s{2}push:\s*$"),
    re.compile(r"(?m)^\s{2}pull_request:\s*$"),
    re.compile(r"(?m)^\s{2}schedule:\s*$"),
    re.compile(r"(?m)^\s{2}workflow_run:\s*$"),
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


def main() -> None:
    if not WORKFLOW.is_file():
        fail(f"workflow does not exist: {WORKFLOW}")

    text = WORKFLOW.read_text(encoding="utf-8")

    for snippet in REQUIRED_WORKFLOW_SNIPPETS:
        if snippet not in text:
            fail(f"required workflow contract is missing: {snippet}")

    lowered = text.lower()

    for token in FORBIDDEN_WORKFLOW_TOKENS:
        if token in lowered:
            fail(f"forbidden workflow command is present: {token}")

    for pattern in AUTOMATIC_TRIGGERS:
        if pattern.search(text):
            fail(
                "automatic workflow trigger is present: "
                f"{pattern.pattern}"
            )

    print("RetainAI manual application-release contract is valid.")


if __name__ == "__main__":
    main()
