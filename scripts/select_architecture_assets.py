#!/usr/bin/env python3
"""Select a small, stable RetainAI subset from official AWS and GCP icon packs."""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


IMAGE_EXTENSIONS = {".png", ".svg"}


@dataclass(frozen=True)
class AssetRequest:
    output_name: str
    required_groups: tuple[tuple[str, ...], ...]
    excluded_tokens: tuple[str, ...] = ()
    prefer_tokens: tuple[str, ...] = ()


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def candidate_text(path: Path) -> str:
    return normalize("/".join(path.parts))


def iter_images(roots: Sequence[Path]) -> Iterable[Path]:
    seen: set[Path] = set()

    for root in roots:
        if not root.exists():
            continue

        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            resolved = path.resolve()
            if resolved in seen:
                continue

            seen.add(resolved)
            yield path


def score(path: Path, request: AssetRequest) -> int | None:
    text = candidate_text(path)

    for group in request.required_groups:
        if not any(normalize(token) in text for token in group):
            return None

    if any(normalize(token) in text for token in request.excluded_tokens):
        return None

    value = 0

    # Prefer vendor service icons over resource/decorative icons.
    if "architecture-service-icons" in text or "architecture_service_icons" in text:
        value += 80
    if "arch_" in path.name.lower() or path.name.lower().startswith("arch"):
        value += 50
    if "64" in path.parts or "64" in path.stem:
        value += 35
    if path.suffix.lower() == ".png":
        value += 20
    if path.suffix.lower() == ".svg":
        value += 18
    if "resource" in text:
        value -= 25
    if "dark" in text or "white" in text:
        value -= 12
    if "deprecated" in text:
        value -= 100

    for token in request.prefer_tokens:
        if normalize(token) in text:
            value += 16

    # Prefer concise service filenames after the semantic score.
    value -= min(len(path.name), 120) // 12
    return value


def choose(roots: Sequence[Path], request: AssetRequest) -> Path:
    ranked: list[tuple[int, Path]] = []

    for path in iter_images(roots):
        value = score(path, request)
        if value is not None:
            ranked.append((value, path))

    ranked.sort(key=lambda item: (-item[0], str(item[1]).lower()))

    if not ranked:
        root_list = ", ".join(str(root) for root in roots)
        raise RuntimeError(
            f"No icon candidate found for {request.output_name!r} under {root_list}."
        )

    selected = ranked[0][1]

    print(f"{request.output_name}: {selected}")
    if len(ranked) > 1:
        print("  alternatives:")
        for value, path in ranked[1:4]:
            print(f"    score={value:>3} {path}")

    return selected


def sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def copy_selected(source: Path, output_directory: Path, stem: str) -> Path:
    output_directory.mkdir(parents=True, exist_ok=True)
    destination = output_directory / f"{stem}{source.suffix.lower()}"
    shutil.copy2(source, destination)
    return destination


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--aws-root", type=Path, required=True)
    parser.add_argument("--gcp-core-root", type=Path, required=True)
    parser.add_argument("--gcp-legacy-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    aws_requests = [
        AssetRequest("lambda", (("aws lambda", "lambda"),), ("lambda edge",)),
        AssetRequest("api-gateway", (("api gateway", "apigateway"),), ("endpoint",)),
        AssetRequest("dynamodb", (("dynamodb", "dynamo db"),), ("table", "attribute")),
        AssetRequest("cloudwatch", (("cloudwatch",),), ("alarm", "event", "logs")),
        AssetRequest(
            "ecr",
            (("elastic container registry", "ecr"),),
            ("image", "registry resource"),
        ),
        AssetRequest(
            "certificate-manager",
            (("certificate manager", "certificatemanager"),),
            ("private certificate authority", "certificate authority"),
        ),
        AssetRequest("bedrock", (("bedrock",),), ("agentcore",)),
        AssetRequest(
            "s3",
            (("simple storage service", "amazon s3", "s3"),),
            ("bucket", "object", "glacier", "vectors", "tables"),
            ("architecture-service-icons",),
        ),
    ]

    gcp_requests = [
        AssetRequest("cloud-run", (("cloud run", "cloudrun"),), ("jobs", "functions")),
        AssetRequest(
            "artifact-registry",
            (("artifact registry", "artifactregistry"),),
        ),
        AssetRequest(
            "secret-manager",
            (("secret manager", "secretmanager"),),
        ),
    ]

    selected_records: list[tuple[str, Path, Path]] = []

    for request in aws_requests:
        source = choose([args.aws_root], request)
        destination = copy_selected(
            source,
            args.output_root / "aws",
            request.output_name,
        )
        selected_records.append(("AWS", source, destination))

    # Prefer the 2025 core icon set; use the official legacy set only when needed.
    for request in gcp_requests:
        try:
            source = choose([args.gcp_core_root], request)
        except RuntimeError:
            source = choose([args.gcp_legacy_root], request)

        destination = copy_selected(
            source,
            args.output_root / "gcp",
            request.output_name,
        )
        selected_records.append(("Google Cloud", source, destination))

    notice_lines = [
        "# Vendor architecture icon notice",
        "",
        "The files in this directory are selected from vendor-provided architecture icon packages.",
        "",
        "## AWS",
        "",
        "Source: https://aws.amazon.com/architecture/icons/",
        "",
        "Package used by the downloader:",
        "`Icon-package_04302026` (the package linked by AWS at generation time).",
        "",
        "AWS permits customers and partners to use its approved architecture assets for diagrams.",
        "Do not recolor, distort, or modify the service marks.",
        "",
        "## Google Cloud",
        "",
        "Source: https://cloud.google.com/icons",
        "",
        "The downloader prefers the official 2025 core product icon package and falls back to",
        "Google's official legacy console icon package when a specific product is not present.",
        "",
        "## Selected files",
        "",
    ]

    for vendor, source, destination in selected_records:
        notice_lines.append(
            f"- **{vendor}** `{destination.name}` ← `{source.name}` "
            f"(SHA-256 `{sha256(destination)}`)"
        )

    notice_lines.extend(
        [
            "",
            "These assets are used only to communicate the RetainAI architecture.",
            "The AWS and Google Cloud names and product marks remain the property of their",
            "respective owners.",
            "",
        ]
    )

    (args.output_root / "NOTICE.md").write_text(
        "\n".join(notice_lines),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
