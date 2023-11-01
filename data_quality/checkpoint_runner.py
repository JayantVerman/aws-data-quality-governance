"""Great Expectations Checkpoint Runner with Quarantine Routing."""

from __future__ import annotations

import json
import re
from pathlib import Path
import pandas as pd

from logging_utils import get_logger

log = get_logger(__name__)


def validate_customer_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Validate dataframe against rules. Split into clean vs quarantine."""
    email_regex = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
    ssn_regex = re.compile(r"^\d{3}-\d{2}-\d{4}$")

    valid_mask = (
        df["customer_id"].notna() &
        df["email"].astype(str).str.match(email_regex) &
        df["ssn"].astype(str).str.match(ssn_regex) &
        df["age"].astype(float).between(18, 90) &
        df["credit_score"].astype(float).between(300, 850)
    )

    clean_df = df[valid_mask].copy()
    quarantine_df = df[~valid_mask].copy()

    total = len(df)
    passed = len(clean_df)
    failed = len(quarantine_df)
    score = (passed / total * 100.0) if total > 0 else 100.0

    metrics = {
        "total_records": total,
        "passed_records": passed,
        "failed_records": failed,
        "quality_score": round(score, 2),
    }

    log.info("Validation complete: score=%.2f%% (passed=%d, failed=%d)", score, passed, failed)
    return clean_df, quarantine_df, metrics


if __name__ == "__main__":
    sample_file = Path("data/synthetic/customers.csv")
    if sample_file.exists():
        data = pd.read_csv(sample_file)
        c, q, m = validate_customer_dataframe(data)
        print("Metrics:", json.dumps(m, indent=2))
