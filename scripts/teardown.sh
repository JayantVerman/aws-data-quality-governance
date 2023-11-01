#!/usr/bin/env bash
# teardown.sh — destroy all AWS infrastructure in reverse order.
# Usage: ./scripts/teardown.sh [confirm]
# Pass "yes" as first arg to actually run terraform destroy.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONFIRM="${1:-}"

if [ "${CONFIRM}" != "yes" ]; then
  echo "DRY RUN — nothing destroyed. To actually destroy, run:"
  echo "  ./scripts/teardown.sh yes"
  exit 0
fi

echo "==> Destroying AWS infrastructure (reverse order)"
cd "${ROOT_DIR}/infra"

echo "  - lake_formation module"
terraform -chdir=modules/lake_formation destroy -auto-approve

echo "  - sns module"
terraform -chdir=modules/sns destroy -auto-approve

echo "  - glue_catalog module"
terraform -chdir=modules/glue_catalog destroy -auto-approve

echo "  - s3 module"
terraform -chdir=modules/s3 destroy -auto-approve

echo "  - iam module"
terraform -chdir=modules/iam destroy -auto-approve

echo "==> All AWS resources destroyed."