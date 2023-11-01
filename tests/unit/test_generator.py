"""Unit tests for synthetic PII data generator."""

from faker import Faker
from data_generator.generate_synthetic_pii import generate_rows


def test_generate_rows_count():
    faker = Faker()
    rows = generate_rows(50, faker)
    assert len(rows) == 50
    assert "ssn" in rows[0]
    assert "email" in rows[0]
