"""Custom OpenLineage Event Emitter."""

from __future__ import annotations

import requests
from logging_utils import get_logger

log = get_logger(__name__)


def emit_lineage_event(job_name: str, inputs: list, outputs: list, url: str = "http://localhost:8080") -> None:
    """Emit OpenLineage run event to Marquez."""
    payload = {
        "eventType": "COMPLETE",
        "job": {"namespace": "aws-data-quality-governance", "name": job_name},
        "inputs": [{"namespace": "s3", "name": i} for i in inputs],
        "outputs": [{"namespace": "s3", "name": o} for o in outputs],
    }
    try:
        res = requests.post(f"{url}/api/v1/lineage", json=payload, timeout=5)
        log.info("Lineage emitted for %s: status %d", job_name, res.status_code)
    except Exception as err:
        log.warning("Lineage emission fallback: %s", err)


if __name__ == "__main__":
    emit_lineage_event("data_quality_transform", ["s3://raw/customers.csv"], ["s3://curated/customers.csv"])
