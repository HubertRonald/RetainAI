#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip setuptools wheel

python -m pip install -e ".[dev,test]"

echo "RetainAI development container is ready."
python --version
python -m pip --version
python -m pytest --version