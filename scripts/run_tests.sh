#!/usr/bin/env bash
set -euo pipefail

echo "==> Running pytest test suite"
pytest tests/ -v --cov=.
