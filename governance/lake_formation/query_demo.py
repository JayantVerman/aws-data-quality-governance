"""Athena Query Comparison Demo (Privileged vs Restricted Role)."""

from __future__ import annotations

from logging_utils import get_logger

log = get_logger(__name__)


def simulate_query_results() -> None:
    """Show before/after query demonstration under Lake Formation security."""
    log.info("=== Query Execution: Privileged Role (Unmasked) ===")
    print("customer_id | first_name | email               | ssn")
    print("CUST-0000001| John       | john.doe@email.com  | 123-45-6789")

    log.info("=== Query Execution: Restricted Role (Column Masked) ===")
    print("customer_id | first_name | email               | ssn")
    print("CUST-0000001| John       | [MASKED]            | [MASKED]")


if __name__ == "__main__":
    simulate_query_results()
