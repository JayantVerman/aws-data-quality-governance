"""Unit tests for boto3 retry client wrapper."""

from aws_client import call_with_retry


def test_call_with_retry_success():
    def dummy_fn(a, b):
        return a + b

    res = call_with_retry(dummy_fn, 5, 10)
    assert res == 15
