"""Thin wrapper around boto3 with retry/backoff and structured logging.

Every AWS call in the project goes through ``aws_client.get_client`` so
that retry/backoff behaviour is consistent and easy to audit.
"""

from __future__ import annotations

import time
from typing import Any, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from logging_utils import get_logger

log = get_logger(__name__)

# Sensible retry policy for transient AWS errors (throttling, etc.).
_RETRY_CONFIG = Config(
    retries={"max_attempts": 5, "mode": "adaptive"},
    connect_timeout=10,
    read_timeout=30,
)


def get_client(service: str, region: Optional[str] = None, **kwargs: Any) -> Any:
    """Return a boto3 client for ``service`` with retry/backoff enabled."""
    return boto3.client(service, region_name=region, config=_RETRY_CONFIG, **kwargs)


def call_with_retry(
    fn,
    *args,
    max_attempts: int = 5,
    base_delay: float = 1.0,
    **kwargs,
):
    """Call ``fn(*args, **kwargs)`` with exponential backoff on ClientError.

    Only retryable error codes are retried — everything else is raised.
    """
    retryable = {"Throttling", "Throttled", "RequestLimitExceeded", "ServiceUnavailable"}
    last_exc: Optional[Exception] = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn(*args, **kwargs)
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code not in retryable:
                raise
            last_exc = exc
            delay = base_delay * (2 ** (attempt - 1))
            log.warning(
                "retryable error on %s (attempt %d/%d): %s — retrying in %.1fs",
                fn.__name__, attempt, max_attempts, code, delay,
            )
            time.sleep(delay)
    raise last_exc  # type: ignore[misc]