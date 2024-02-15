"""Unit tests for boto3 retry client wrapper."""

from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from aws_client import call_with_retry, get_client


def test_call_with_retry_success():
    """Verify successful function call returns result."""
    def dummy_fn(a, b):
        return a + b

    res = call_with_retry(dummy_fn, 5, 10)
    assert res == 15


def test_call_with_retry_non_retryable_error():
    """Verify non-retryable errors are raised immediately."""
    def failing_fn():
        error_response = {"Error": {"Code": "AccessDenied", "Message": "Access Denied"}}
        raise ClientError(error_response, "GetObject")

    try:
        call_with_retry(failing_fn)
        assert False, "Should have raised ClientError"
    except ClientError as e:
        assert e.response["Error"]["Code"] == "AccessDenied"


@patch("aws_client.time.sleep")
def test_call_with_retry_retryable_error(mock_sleep):
    """Verify retryable errors trigger retries with exponential backoff."""
    call_count = 0

    def throttling_fn():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            error_response = {"Error": {"Code": "Throttling", "Message": "Rate exceeded"}}
            raise ClientError(error_response, "GetObject")
        return "success"

    result = call_with_retry(throttling_fn, max_attempts=5)
    assert result == "success"
    assert call_count == 3
    assert mock_sleep.call_count == 2


@patch("aws_client.time.sleep")
def test_call_with_retry_exhausts_attempts(mock_sleep):
    """Verify exception is raised after max attempts exhausted."""
    def always_fail():
        error_response = {"Error": {"Code": "ServiceUnavailable", "Message": "Service down"}}
        raise ClientError(error_response, "GetObject")

    try:
        call_with_retry(always_fail, max_attempts=3, base_delay=0.01)
        assert False, "Should have raised ClientError"
    except ClientError:
        # Sleeps after each failed attempt (3 attempts = 3 sleeps)
        assert mock_sleep.call_count == 3



def test_get_client_returns_boto3_client():
    """Verify get_client returns a boto3 client."""
    client = get_client("s3", region="us-east-1")
    assert client is not None
    assert hasattr(client, "get_object")
    assert hasattr(client, "put_object")

