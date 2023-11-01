#!/usr/bin/env bash
# setup.sh — one-time environment setup for aws-data-quality-governance.
# Run after cloning: ./scripts/setup.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "==> Setting up Python virtual environment"
python3 -m venv "${ROOT_DIR}/.venv"
source "${ROOT_DIR}/.venv/bin/activate"

echo "==> Upgrading pip"
pip install --upgrade pip

echo "==> Installing Python dependencies"
if [ -f "${ROOT_DIR}/requirements.txt" ]; then
  pip install -r "${ROOT_DIR}/requirements.txt"
fi

echo "==> Installing pre-commit hooks"
if [ -f "${ROOT_DIR}/.pre-commit-config.yaml" ]; then
  pre-commit install
fi

echo "==> Terraform provider plugins"
if [ -d "${ROOT_DIR}/infra" ]; then
  cd "${ROOT_DIR}/infra" && terraform init
fi

echo "==> Done. Activate with: source .venv/bin/activate"