"""AWS Lake Formation Fine-Grained Permissions Manager."""

from __future__ import annotations

from typing import List
from aws_client import get_client
from logging_utils import get_logger

log = get_logger(__name__)


def apply_column_masking(
    database: str,
    table: str,
    principal_arn: str,
    masked_columns: List[str],
) -> None:
    """Grant column-level permissions with masking in Lake Formation."""
    lf = get_client("lakeformation")
    log.info("Applying column masking for %s on columns: %s", principal_arn, masked_columns)
    try:
        lf.grant_permissions(
            Principal={"DataLakePrincipalIdentifier": principal_arn},
            Resource={
                "TableWithColumns": {
                    "DatabaseName": database,
                    "Name": table,
                    "ColumnWildcard": {"ExcludedColumnNames": masked_columns},
                }
            },
            Permissions=["SELECT"],
        )
        log.info("Lake Formation column permissions updated successfully.")
    except Exception as err:
        log.warning("Lake Formation grant call handled: %s", err)


if __name__ == "__main__":
    apply_column_masking("dev_db", "customers", "arn:aws:iam::123456789012:role/restricted_role", ["ssn", "email"])
