#!/usr/bin/env bash
# seed_data.sh — generate synthetic PII data and upload to S3 raw bucket.
# Usage: ./scripts/seed_data.sh [rows]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
ROWS="${1:-1000}"

echo "==> Generating ${ROWS} synthetic customer rows"
source "${ROOT_DIR}/.venv/bin/activate" 2>/dev/null || true
python "${ROOT_DIR}/data_generator/generate_synthetic_pii.py" \
  --rows "${ROWS}" \
  --out "${ROOT_DIR}/data/synthetic/customers.csv"

echo "==> Uploading to S3 raw bucket"
BUCKET="${RAW_S3_BUCKET:-$(terraform -chdir="${ROOT_DIR}/infra" output -raw raw_bucket_name 2>/dev/null)}"
if [ -z "${BUCKET}" ]; then
  echo "RAW_S3_BUCKET not set and terraform output unavailable; set RAW_S3_BUCKET env var"
  exit 1
fi
aws s3 cp "${ROOT_DIR}/data/synthetic/customers.csv" "s3://${BUCKET}/raw/customers.csv"

echo "==> Done. File at s3://${BUCKET}/raw/customers.csv"