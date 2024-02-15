"""Unit tests for Macie findings parser."""

from governance.macie.parse_findings import parse_macie_findings


def test_parse_macie_findings_empty():
    """Verify empty findings returns default PII columns."""
    res = parse_macie_findings([])
    assert "pii_columns_detected" in res
    assert len(res["pii_columns_detected"]) > 0


def test_parse_macie_findings_with_data():
    """Verify parsing extracts PII columns from findings."""
    mock_findings = [
        {
            "severity": {"description": "HIGH"},
            "classificationDetails": {
                "result": {
                    "sensitiveData": [
                        {"location": {"column": {"name": "ssn"}}},
                        {"location": {"column": {"name": "email"}}},
                    ]
                }
            },
        },
        {
            "severity": {"description": "MEDIUM"},
            "classificationDetails": {
                "result": {
                    "sensitiveData": [
                        {"location": {"column": {"name": "phone"}}},
                    ]
                }
            },
        },
    ]
    res = parse_macie_findings(mock_findings)
    assert "ssn" in res["pii_columns_detected"]
    assert "email" in res["pii_columns_detected"]
    assert "phone" in res["pii_columns_detected"]
    assert res["total_findings"] == 2
    assert res["high_severity_count"] == 1
    assert res["requires_alert"] is True


def test_parse_macie_findings_no_high_severity():
    """Verify alert flag is False when no HIGH severity findings."""
    mock_findings = [
        {
            "severity": {"description": "LOW"},
            "classificationDetails": {
                "result": {
                    "sensitiveData": [{"location": {"column": {"name": "address"}}}]
                }
            },
        }
    ]
    res = parse_macie_findings(mock_findings)
    assert res["high_severity_count"] == 0
    assert res["requires_alert"] is False


def test_parse_macie_findings_missing_column_name():
    """Verify findings with missing column names are handled gracefully."""
    mock_findings = [
        {
            "severity": {"description": "HIGH"},
            "classificationDetails": {
                "result": {
                    "sensitiveData": [{"location": {"column": {}}}]
                }
            },
        }
    ]
    res = parse_macie_findings(mock_findings)
    assert res["total_findings"] == 1
    assert res["high_severity_count"] == 1

