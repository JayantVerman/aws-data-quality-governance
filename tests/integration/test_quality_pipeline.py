"""Integration test for Great Expectations checkpoint runner."""

import pandas as pd
from data_quality.checkpoint_runner import validate_customer_dataframe


def test_validate_customer_dataframe():
    df = pd.DataFrame([
        {"customer_id": "CUST-1", "email": "a@b.com", "ssn": "123-45-6789", "age": 30, "credit_score": 700},
        {"customer_id": "CUST-2", "email": "bad_email", "ssn": "123", "age": 100, "credit_score": 200},
    ])
    clean, quar, metrics = validate_customer_dataframe(df)
    assert len(clean) == 1
    assert len(quar) == 1
    assert metrics["quality_score"] == 50.0
