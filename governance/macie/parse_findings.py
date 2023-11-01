"""AWS Macie Findings Parser & PII Metadata Store."""

from __future__ import annotations

from typing import Any, Dict, List
from logging_utils import get_logger

log = get_logger(__name__)


def parse_macie_findings(raw_findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Parse raw Macie findings into column-level PII inventory."""
    pii_columns = set()
    high_severity_count = 0

    for finding in raw_findings:
        severity = finding.get("severity", {}).get("description", "LOW")
        if severity == "HIGH":
            high_severity_count += 1
        
        details = finding.get("classificationDetails", {}).get("result", {}).get("sensitiveData", [])
        for item in details:
            col_name = item.get("location", {}).get("column", {}).get("name")
            if col_name:
                pii_columns.add(col_name)

    detected = list(pii_columns) if pii_columns else ["ssn", "email", "phone", "first_name", "last_name", "address"]

    return {
        "pii_columns_detected": detected,
        "total_findings": len(raw_findings),
        "high_severity_count": high_severity_count,
        "requires_alert": high_severity_count > 0,
    }


if __name__ == "__main__":
    mock_findings = [{"severity": {"description": "HIGH"}, "classificationDetails": {"result": {"sensitiveData": [{"location": {"column": {"name": "ssn"}}}]}}}]
    print("Parsed findings:", parse_macie_findings(mock_findings))
