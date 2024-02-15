"""Integration test for Great Expectations checkpoint runner."""

import pandas as pd
from data_quality.checkpoint_runner import validate_customer_dataframe


def test_validate_customer_dataframe():
    """Verify validation splits data into clean and quarantine sets."""
    df = pd.DataFrame([
        {"customer_id": "CUST-1", "email": "a@b.com", "ssn": "123-45-6789", "age": 30, "credit_score": 700},
        {"customer_id": "CUST-2", "email": "bad_email", "ssn": "123", "age": 100, "credit_score": 200},
    ])
    clean, quar, metrics = validate_customer_dataframe(df)
    assert len(clean) == 1
    assert len(quar) == 1
    assert metrics["quality_score"] == 50.0


def test_validate_all_valid_records():
    """Verify all records pass when data is valid."""
    df = pd.DataFrame([
        {"customer_id": "CUST-1", "email": "a@b.com", "ssn": "123-45-6789", "age": 30, "credit_score": 700},
        {"customer_id": "CUST-2", "email": "c@d.com", "ssn": "987-65-4321", "age": 45, "credit_score": 650},
    ])
    clean, quar, metrics = validate_customer_dataframe(df)
    assert len(clean) == 2
    assert len(quar) == 0
    assert metrics["quality_score"] == 100.0


def test_validate_all_invalid_records():
    """Verify all records fail when data is invalid."""
    df = pd.DataFrame([
        {"customer_id": "CUST-1", "email": "bad", "ssn": "invalid", "age": 10, "credit_score": 100},
        {"customer_id": "CUST-2", "email": "also_bad", "ssn": "nope", "age": 200, "credit_score": 900},
    ])
    clean, quar, metrics = validate_customer_dataframe(df)
    assert len(clean) == 0
    assert len(quar) == 2
    assert metrics["quality_score"] == 0.0


def test_validate_empty_dataframe():
    """Verify validation handles empty dataframe."""
    df = pd.DataFrame(columns=["customer_id", "email", "ssn", "age", "credit_score"])
    clean, quar, metrics = validate_customer_dataframe(df)
    assert len(clean) == 0
    assert len(quar) == 0
    assert metrics["quality_score"] == 100.0  # Empty set defaults to 100%


def test_validate_boundary_values():
    """Verify boundary values are handled correctly."""
    df = pd.DataFrame([
        {"customer_id": "CUST-1", "email": "a@b.com", "ssn": "123-45-6789", "age": 18, "credit_score": 300},  # Min boundaries
        {"customer_id": "CUST-2", "email": "c@d.com", "ssn": "987-65-4321", "age": 90, "credit_score": 850},  # Max boundaries
    ])
    clean, quar, metrics = validate_customer_dataframe(df)
    assert len(clean) == 2
    assert len(quar) == 0

