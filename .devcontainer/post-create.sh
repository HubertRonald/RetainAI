#!/usr/bin/env bash
set -Eeuo pipefail

cd /workspace

echo "Checking /workspace/.venv mount..."

if ! grep -q " /workspace/.venv " /proc/mounts; then
  echo "ERROR: /workspace/.venv is not mounted as a Docker volume."
  echo "The host macOS .venv is still leaking into the DevContainer."
  echo "Check .devcontainer/devcontainer.json."
  exit 1
fi

sudo chown -R "$(id -u):$(id -g)" /workspace/.venv || true

EXPECTED_VENV="/workspace/.venv"

if [ -f ".venv/bin/activate" ]; then
  DETECTED_VENV="$(
    sed -n 's/^VIRTUAL_ENV=//p' ".venv/bin/activate" \
      | head -n 1 \
      | tr -d '"'
  )"

  if [ -n "${DETECTED_VENV}" ] && [ "${DETECTED_VENV}" != "${EXPECTED_VENV}" ]; then
    echo "ERROR: Existing virtual environment points to a different path."
    echo "Detected: ${DETECTED_VENV}"
    echo "Expected: ${EXPECTED_VENV}"
    echo
    echo "This usually means a host virtual environment leaked into the DevContainer."
    echo "Make sure /workspace/.venv is mounted as a Docker volume."
    exit 1
  fi
fi

if [ ! -x ".venv/bin/python" ]; then
  echo "Creating Linux virtualenv at /workspace/.venv..."
  /usr/local/bin/python -m venv .venv
fi

# shellcheck disable=SC1091
. ./.venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev,test]"

if [ -f "infra/multicloud-pulumi-python/requirements.txt" ]; then
  python -m pip install -r infra/multicloud-pulumi-python/requirements.txt
fi

echo
echo "RetainAI multi-cloud development container is ready."
echo "VIRTUAL_ENV=${VIRTUAL_ENV}"
which python
which pip
python -m pip --version
aws --version
gcloud --version | head -n 1
pulumi version
docker --version
git --version
gh --version
