#!/usr/bin/env bash

set -Eeuo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || printf '/workspace')"
CACHE_DIR="${ARCHITECTURE_ICON_CACHE:-${ROOT_DIR}/.cache/architecture-icons}"
VENDOR_DIR="${ROOT_DIR}/docs/architecture/assets/vendor"
PYTHON_BIN="${PYTHON_BIN:-python}"

AWS_ICON_URL="${AWS_ICON_URL:-https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/architecture/approved/architecture-icons/Icon-package_04302026.4705b90f5aa45b019271a2699e9ce9b97b941ee1.zip}"
GCP_CORE_URL="${GCP_CORE_URL:-https://services.google.com/fh/files/misc/core-products-icons.zip}"
GCP_LEGACY_URL="${GCP_LEGACY_URL:-https://services.google.com/fh/files/misc/google-cloud-legacy-icons.zip}"

mkdir -p \
  "${CACHE_DIR}/downloads" \
  "${CACHE_DIR}/expanded/aws" \
  "${CACHE_DIR}/expanded/gcp-core" \
  "${CACHE_DIR}/expanded/gcp-legacy" \
  "${VENDOR_DIR}/aws" \
  "${VENDOR_DIR}/gcp"

require_command() {
  local name="$1"

  if ! command -v "${name}" >/dev/null 2>&1; then
    printf 'ERROR: required command not found: %s\n' "${name}" >&2
    return 2
  fi
}

require_command curl
require_command unzip
require_command "${PYTHON_BIN}"

download() {
  local url="$1"
  local destination="$2"

  if [[ -s "${destination}" ]]; then
    printf 'Using cached download: %s\n' "${destination}"
    return 0
  fi

  printf 'Downloading official icon package:\n  %s\n' "${url}"

  curl \
    --fail \
    --location \
    --retry 4 \
    --retry-delay 2 \
    --connect-timeout 20 \
    --output "${destination}.partial" \
    "${url}"

  mv \
    "${destination}.partial" \
    "${destination}"
}

expand() {
  local archive="$1"
  local destination="$2"
  local marker="${destination}/.expanded"

  if [[ -f "${marker}" ]]; then
    printf 'Using expanded package: %s\n' "${destination}"
    return 0
  fi

  rm -rf "${destination}"
  mkdir -p "${destination}"

  unzip \
    -q \
    "${archive}" \
    -d "${destination}"

  touch "${marker}"
}

AWS_ZIP="${CACHE_DIR}/downloads/aws-architecture-icons.zip"
GCP_CORE_ZIP="${CACHE_DIR}/downloads/gcp-core-product-icons.zip"
GCP_LEGACY_ZIP="${CACHE_DIR}/downloads/gcp-legacy-product-icons.zip"

download "${AWS_ICON_URL}" "${AWS_ZIP}"
download "${GCP_CORE_URL}" "${GCP_CORE_ZIP}"
download "${GCP_LEGACY_URL}" "${GCP_LEGACY_ZIP}"

expand "${AWS_ZIP}" "${CACHE_DIR}/expanded/aws"
expand "${GCP_CORE_ZIP}" "${CACHE_DIR}/expanded/gcp-core"
expand "${GCP_LEGACY_ZIP}" "${CACHE_DIR}/expanded/gcp-legacy"

"${PYTHON_BIN}" \
  "${ROOT_DIR}/scripts/select_architecture_assets.py" \
  --aws-root "${CACHE_DIR}/expanded/aws" \
  --gcp-core-root "${CACHE_DIR}/expanded/gcp-core" \
  --gcp-legacy-root "${CACHE_DIR}/expanded/gcp-legacy" \
  --output-root "${VENDOR_DIR}"

printf '\nSelected official assets:\n'
find "${VENDOR_DIR}" \
  -maxdepth 2 \
  -type f \
  \( -name '*.png' -o -name '*.svg' -o -name 'NOTICE.md' \) \
  -print \
  | sort
