#!/usr/bin/env bash

set -Eeuo pipefail

ROOT_DIR="$(
  git rev-parse --show-toplevel 2>/dev/null \
    || printf '/workspace'
)"

AWS_ROOT="${AWS_ARCHITECTURE_ICON_ROOT:-${ROOT_DIR}/.cache/architecture-icons/expanded/aws}"

OUTPUT_DIR="${AWS_ARCHITECTURE_VENDOR_DIR:-${ROOT_DIR}/docs/architecture/assets/vendor/aws}"

PNG_SIZE="${ARCHITECTURE_ICON_PNG_SIZE:-160}"
PYTHON_BIN="${PYTHON_BIN:-python}"

if [[ ! -d "${AWS_ROOT}" ]]; then
  printf 'ERROR: expanded AWS icon package not found: %s\n' \
    "${AWS_ROOT}" >&2
  printf 'Run the official package downloader first.\n' >&2
  exit 2
fi

mkdir -p "${OUTPUT_DIR}"

export AWS_ROOT
export OUTPUT_DIR
export PNG_SIZE

"${PYTHON_BIN}" - <<'PY'
from __future__ import annotations

import hashlib
import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


aws_root = Path(os.environ["AWS_ROOT"])
output_dir = Path(os.environ["OUTPUT_DIR"])
png_size = int(os.environ["PNG_SIZE"])

if png_size < 64:
    raise RuntimeError(
        "ARCHITECTURE_ICON_PNG_SIZE must be at least 64."
    )

# Stable output name -> exact AWS architecture service icon stem.
services = {
    "lambda": "Arch_AWS-Lambda_64",
    "api-gateway": "Arch_Amazon-API-Gateway_64",
    "dynamodb": "Arch_Amazon-DynamoDB_64",
    "cloudwatch": "Arch_Amazon-CloudWatch_64",
    "ecr": "Arch_Amazon-Elastic-Container-Registry_64",
    "certificate-manager": "Arch_AWS-Certificate-Manager_64",
    "bedrock": "Arch_Amazon-Bedrock_64",
    "s3": "Arch_Amazon-Simple-Storage-Service_64",
}


def valid_source(path: Path) -> bool:
    if not path.is_file():
        return False

    if "__MACOSX" in path.parts:
        return False

    if path.name.startswith("._"):
        return False

    return True


def find_exact(stem: str) -> tuple[Path, str]:
    # Prefer official SVG.
    svg_candidates = sorted(
        path
        for path in aws_root.rglob(f"{stem}.svg")
        if valid_source(path)
    )

    if len(svg_candidates) == 1:
        return svg_candidates[0], "svg"

    if len(svg_candidates) > 1:
        raise RuntimeError(
            f"Multiple exact SVG candidates for {stem}: "
            + ", ".join(str(path) for path in svg_candidates)
        )

    # Prefer AWS-provided @5x PNG before the 64px PNG.
    high_res_candidates = sorted(
        path
        for path in aws_root.rglob(f"{stem}@5x.png")
        if valid_source(path)
    )

    if len(high_res_candidates) == 1:
        return high_res_candidates[0], "png"

    if len(high_res_candidates) > 1:
        raise RuntimeError(
            f"Multiple exact @5x candidates for {stem}: "
            + ", ".join(str(path) for path in high_res_candidates)
        )

    png_candidates = sorted(
        path
        for path in aws_root.rglob(f"{stem}.png")
        if valid_source(path)
    )

    if len(png_candidates) == 1:
        return png_candidates[0], "png"

    if not png_candidates:
        raise RuntimeError(
            f"No exact official icon found for {stem}."
        )

    raise RuntimeError(
        f"Multiple exact PNG candidates for {stem}: "
        + ", ".join(str(path) for path in png_candidates)
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def validate_svg(path: Path) -> None:
    if path.stat().st_size < 300:
        raise RuntimeError(
            f"SVG too small: {path}"
        )

    root = ET.parse(path).getroot()

    if not root.tag.lower().endswith("svg"):
        raise RuntimeError(
            f"Not an SVG document: {path}"
        )


def normalize_png(
    source: Path,
    destination: Path,
    size: int,
) -> None:
    with Image.open(source) as image:
        rgba = image.convert("RGBA")

    if rgba.getbbox() is None:
        raise RuntimeError(
            f"Source image is blank: {source}"
        )

    rgba.thumbnail(
        (size, size),
        Image.Resampling.LANCZOS,
    )

    canvas = Image.new(
        "RGBA",
        (size, size),
        (0, 0, 0, 0),
    )

    offset = (
        (size - rgba.width) // 2,
        (size - rgba.height) // 2,
    )

    canvas.alpha_composite(
        rgba,
        offset,
    )

    if canvas.getbbox() is None:
        raise RuntimeError(
            f"Normalized image is blank: {source}"
        )

    canvas.save(
        destination,
        format="PNG",
        optimize=True,
    )


def svg_to_png(
    source: Path,
    destination: Path,
    size: int,
) -> None:
    try:
        import cairosvg
    except ImportError as error:
        raise RuntimeError(
            "CairoSVG is required. Install "
            "requirements/architecture-diagrams.txt."
        ) from error

    cairosvg.svg2png(
        url=str(source),
        write_to=str(destination),
        output_width=size,
        output_height=size,
    )


def validate_png(path: Path) -> tuple[int, int, object]:
    if path.stat().st_size < 300:
        raise RuntimeError(
            f"PNG too small: {path}"
        )

    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        bbox = rgba.getbbox()

        if bbox is None:
            raise RuntimeError(
                f"PNG is blank: {path}"
            )

        return rgba.width, rgba.height, bbox


records = []

for output_name, exact_stem in services.items():
    source, source_kind = find_exact(exact_stem)

    png_destination = output_dir / f"{output_name}.png"
    svg_destination = output_dir / f"{output_name}.svg"

    for stale in (
        png_destination,
        svg_destination,
    ):
        if stale.exists():
            stale.unlink()

    if source_kind == "svg":
        shutil.copy2(
            source,
            svg_destination,
        )
        validate_svg(svg_destination)

        svg_to_png(
            svg_destination,
            png_destination,
            png_size,
        )
    else:
        normalize_png(
            source,
            png_destination,
            png_size,
        )

    width, height, bbox = validate_png(
        png_destination
    )

    records.append(
        {
            "name": output_name,
            "source": str(source),
            "source_kind": source_kind,
            "png": str(png_destination),
            "size": f"{width}x{height}",
            "bbox": str(bbox),
            "bytes": png_destination.stat().st_size,
            "sha256": sha256(png_destination),
        }
    )

    print(
        f"{output_name:22} "
        f"{width}x{height} "
        f"bbox={bbox} "
        f"bytes={png_destination.stat().st_size}"
    )
    print(
        f"  source: {source}"
    )

notice = output_dir.parent / "NOTICE.md"

lines = [
    "# Vendor architecture icon notice",
    "",
    "AWS assets were selected from the official AWS Architecture",
    "Icons package using exact architecture service icon names.",
    "",
    "AppleDouble files under `__MACOSX` and files beginning with",
    "`._` are explicitly rejected.",
    "",
    "## AWS selected assets",
    "",
]

for record in records:
    lines.append(
        f"- `{record['name']}.png` from "
        f"`{Path(record['source']).name}`; "
        f"{record['size']}; SHA-256 `{record['sha256']}`."
    )

lines.extend(
    [
        "",
        "The service marks are not recolored.",
        "",
    ]
)

notice.write_text(
    "\n".join(lines),
    encoding="utf-8",
)

print()
print(f"Updated notice: {notice}")
PY

printf '\n=== Repaired AWS assets ===\n'

find "${OUTPUT_DIR}" \
  -maxdepth 1 \
  -type f \
  \( -name '*.png' -o -name '*.svg' \) \
  -print \
  | sort
