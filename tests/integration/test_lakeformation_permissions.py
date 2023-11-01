"""Integration test for Lake Formation permissions helper."""

from governance.lake_formation.permissions_manager import apply_column_masking


def test_apply_column_masking_dryrun():
    apply_column_masking("test_db", "test_table", "arn:aws:iam::123:role/test", ["ssn"])
