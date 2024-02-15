"""Unit tests for synthetic PII data generator."""

import re
from pathlib import Path
from faker import Faker
from data_generator.generate_synthetic_pii import generate_rows, write_csv, FIELDS
from data_generator.schema import CustomerRecord


def test_generate_rows_count():
    """Verify correct number of rows is generated."""
    faker = Faker()
    rows = generate_rows(50, faker)
    assert len(rows) == 50
    assert "ssn" in rows[0]
    assert "email" in rows[0]


def test_generate_rows_fields():
    """Verify all expected fields are present in each row."""
    faker = Faker()
    rows = generate_rows(10, faker)
    for row in rows:
        for field in FIELDS:
            assert field in row, f"Missing field: {field}"


def test_generate_rows_email_format():
    """Verify email addresses have valid format."""
    faker = Faker()
    rows = generate_rows(20, faker)
    email_regex = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
    for row in rows:
        assert email_regex.match(row["email"]), f"Invalid email: {row['email']}"


def test_generate_rows_ssn_format():
    """Verify SSN has proper format (XXX-XX-XXXX)."""
    faker = Faker()
    rows = generate_rows(20, faker)
    ssn_regex = re.compile(r"^\d{3}-\d{2}-\d{4}$")
    for row in rows:
        assert ssn_regex.match(row["ssn"]), f"Invalid SSN: {row['ssn']}"


def test_generate_rows_age_range():
    """Verify age is within expected range."""
    faker = Faker()
    rows = generate_rows(50, faker)
    for row in rows:
        age = int(row["age"])
        assert 18 <= age <= 90, f"Age out of range: {age}"


def test_generate_rows_credit_score_range():
    """Verify credit score is within expected range."""
    faker = Faker()
    rows = generate_rows(50, faker)
    for row in rows:
        score = int(row["credit_score"])
        assert 300 <= score <= 850, f"Credit score out of range: {score}"


def test_generate_rows_customer_id_format():
    """Verify customer ID has proper format."""
    faker = Faker()
    rows = generate_rows(10, faker)
    for i, row in enumerate(rows):
        assert row["customer_id"] == f"CUST-{i + 1:07d}"


def test_generate_rows_deterministic_with_seed():
    """Verify generation is deterministic when seed is fixed."""
    Faker.seed(42)
    faker1 = Faker()
    rows1 = generate_rows(10, faker1)

    Faker.seed(42)
    faker2 = Faker()
    rows2 = generate_rows(10, faker2)

    assert rows1 == rows2


def test_write_csv(tmp_path):
    """Verify CSV file is written correctly."""
    faker = Faker()
    rows = generate_rows(5, faker)
    out_path = tmp_path / "test_output.csv"
    write_csv(rows, out_path)
    assert out_path.exists()
    assert out_path.stat().st_size > 0


def test_write_csv_creates_parent_dirs(tmp_path):
    """Verify write_csv creates parent directories."""
    faker = Faker()
    rows = generate_rows(5, faker)
    out_path = tmp_path / "subdir" / "nested" / "test_output.csv"
    write_csv(rows, out_path)
    assert out_path.exists()


def test_customer_record_to_dict():
    """Verify CustomerRecord dataclass converts to dict correctly."""
    record = CustomerRecord(
        customer_id="CUST-0000001",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="555-123-4567",
        address="123 Main St",
        city="Springfield",
        state="IL",
        zip="62701",
        ssn="123-45-6789",
        age=30,
        account_balance=1000.50,
        credit_score=700,
        signup_date="2023-01-15",
    )
    d = record.to_dict()
    assert d["customer_id"] == "CUST-0000001"
    assert d["email"] == "john@example.com"
    assert d["age"] == 30
    assert isinstance(d, dict)

