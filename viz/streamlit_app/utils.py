"""Streamlit Dashboard Helpers."""

from __future__ import annotations

import requests


def get_marquez_jobs(url: str = "http://localhost:8080") -> list:
    """Fetch active lineage jobs from Marquez API."""
    try:
        r = requests.get(f"{url}/api/v1/namespaces/aws-data-quality-governance/jobs", timeout=3)
        return r.json().get("jobs", [])
    except Exception:
        return []
