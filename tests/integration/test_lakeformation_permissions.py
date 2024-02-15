"""Integration test for Lake Formation permissions helper."""

from unittest.mock import patch, MagicMock
from governance.lake_formation.permissions_manager import apply_column_masking


@patch("governance.lake_formation.permissions_manager.get_client")
def test_apply_column_masking_dryrun(mock_get_client):
    """Verify apply_column_masking runs without error."""
    mock_lf = MagicMock()
    mock_get_client.return_value = mock_lf
    apply_column_masking("test_db", "test_table", "arn:aws:iam::123:role/test", ["ssn"])


@patch("governance.lake_formation.permissions_manager.get_client")
def test_apply_column_masking_calls_grant_permissions(mock_get_client):
    """Verify Lake Formation grant_permissions is called correctly."""
    mock_lf = MagicMock()
    mock_get_client.return_value = mock_lf

    apply_column_masking(
        "dev_db",
        "customers",
        "arn:aws:iam::123456789012:role/restricted_role",
        ["ssn", "email"],
    )

    mock_get_client.assert_called_once_with("lakeformation")
    mock_lf.grant_permissions.assert_called_once()

    call_args = mock_lf.grant_permissions.call_args
    assert call_args[1]["Principal"]["DataLakePrincipalIdentifier"] == "arn:aws:iam::123456789012:role/restricted_role"
    assert call_args[1]["Resource"]["TableWithColumns"]["DatabaseName"] == "dev_db"
    assert call_args[1]["Resource"]["TableWithColumns"]["Name"] == "customers"
    assert "ssn" in call_args[1]["Resource"]["TableWithColumns"]["ColumnWildcard"]["ExcludedColumnNames"]
    assert "email" in call_args[1]["Resource"]["TableWithColumns"]["ColumnWildcard"]["ExcludedColumnNames"]
    assert call_args[1]["Permissions"] == ["SELECT"]

