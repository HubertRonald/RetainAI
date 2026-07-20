#!/usr/bin/env bash

set -Eeuo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || printf '/workspace')"
PYTHON_BIN="${PYTHON_BIN:-python}"

if ! "${PYTHON_BIN}" -c 'from PIL import Image' >/dev/null 2>&1; then
  printf 'ERROR: Pillow is required in the active Python environment.\n' >&2
  printf 'Activate the project virtual environment and run:\n' >&2
  printf '  python -m pip install "Pillow>=10,<13"\n' >&2
  return 2 2>/dev/null || exit 2
fi

required_assets=(
  "aws/lambda"
  "aws/api-gateway"
  "aws/dynamodb"
  "aws/cloudwatch"
  "aws/ecr"
  "aws/certificate-manager"
  "aws/bedrock"
  "aws/s3"
  "gcp/cloud-run"
  "gcp/artifact-registry"
  "gcp/secret-manager"
)

missing=0

for relative_stem in "${required_assets[@]}"; do
  asset_root="${ROOT_DIR}/docs/architecture/assets/vendor/${relative_stem}"

  if [[ ! -s "${asset_root}.png" && ! -s "${asset_root}.svg" ]]; then
    printf 'Missing asset: %s.[png|svg]\n' "${asset_root}" >&2
    missing=1
  fi
done

if [[ "${missing}" == "1" ]]; then
  printf '\nRun the official asset downloader first:\n' >&2
  printf '  ./scripts/download_architecture_assets.sh\n' >&2
  return 3 2>/dev/null || exit 3
fi

"${PYTHON_BIN}" \
  "${ROOT_DIR}/scripts/render_architecture_diagrams.py" \
  --root "${ROOT_DIR}" \
  --diagram all \
  --png-scale "${ARCHITECTURE_PNG_SCALE:-1.0}"

printf '\nRendered architecture assets:\n'
find "${ROOT_DIR}/figs" \
  -maxdepth 2 \
  -type f \
  \( -name '*.svg' -o -name '*.png' \) \
  -print \
  | sort
