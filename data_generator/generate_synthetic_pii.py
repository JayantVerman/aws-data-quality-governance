"""Synthetic PII-rich customer dataset generator.

Generates a clearly-synthetic but PII-rich CSV dataset so that Great
Expectations validation, AWS Macie classification, and Lake Formation
column-level masking all have something real to operate on.

Run directly:

    python -m data_generator.generate_synthetic_pii --rows 1000 --out data/synthetic/customers.csv

The generator is deterministic when ``--seed`` is fixed, which makes
regression testing of the downstream pipeline reproducible.
"""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
from typing import Optional

from faker import Faker

from common.logging_utils import get_logger

log = get_logger(__name__)

# Fields deliberately chosen to exercise every governance primitive:
#   - name, email, phone, address, ssn -> PII (Macie should flag these)
#   - age, balance, credit_score -> data-quality checks (GE suites)
#   - customer_id -> primary key, no PII
FIELDS = [
    "customer_id",
    "first_name",
    "last_name",
    "email",
    "phone",
    "address",
    "city",
    "state",
    "zip",
    "ssn",
    "age",
    "account_balance",
    "credit_score",
    "signup_date",
]


def generate_rows(num_rows: int, faker: Faker) -> list[dict[str, str]]:
    """Generate ``num_rows`` synthetic customer records."""
    rows: list[dict[str, str]] = []
    for i in range(num_rows):
        rows.append(
            {
                "customer_id": f"CUST-{i + 1:07d}",
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "email": faker.email(),
                "phone": faker.phone_number(),
                "address": faker.address().replace("\n", ", "),
                "city": faker.city(),
                "state": faker.state(),
                "zip": faker.postcode(),
                "ssn": faker.ssn(),
                "age": str(faker.random_int(min=18, max=90)),
                "account_balance": f"{faker.random_int(min=0, max=100000):.2f}",
                "credit_score": str(faker.random_int(min=300, max=850)),
                "signup_date": faker.date_between(start_date="-3y", end_date="today").isoformat(),
            }
        )
    return rows


def write_csv(rows: list[dict[str, str]], out_path: Path) -> None:
    """Write rows to ``out_path`` (parent dirs created on demand)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    log.info("wrote %d rows to %s", len(rows), out_path)


def main(rows: int, out: str, seed: Optional[int]) -> None:
    """Entry point — generate the dataset and write it to disk."""
    if seed is not None:
        Faker.seed(seed)
    faker = Faker()
    log.info("generating %d synthetic customer rows (seed=%s)", rows, seed)
    data = generate_rows(rows, faker)
    write_csv(data, Path(out))
    log.info("done — file at %s", out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=1000, help="number of rows to generate")
    parser.add_argument(
        "--out",
        type=str,
        default="data/synthetic/customers.csv",
        help="output CSV path",
    )
    parser.add_argument("--seed", type=int, default=None, help="reproducibility seed")
    args = parser.parse_args()
    main(args.rows, args.out, args.seed)