#!/usr/bin/env bash
set -euo pipefail

echo "==> Executing standalone data governance pipeline"
python -m data_generator.generate_synthetic_pii --rows 1000
python data_quality/checkpoint_runner.py
python governance/macie/trigger_scan.py
python governance/lake_formation/query_demo.py
