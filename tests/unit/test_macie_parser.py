"""Unit tests for Macie findings parser."""

from governance.macie.parse_findings import parse_macie_findings


def test_parse_macie_findings_empty():
    res = parse_macie_findings([])
    assert "pii_columns_detected" in res
    assert len(res["pii_columns_detected"]) > 0
