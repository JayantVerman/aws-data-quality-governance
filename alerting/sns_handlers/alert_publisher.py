"""SNS Governance Alert Publisher."""

from __future__ import annotations

import json
from aws_client import get_client
from logging_utils import get_logger

log = get_logger(__name__)


def publish_alert(topic_arn: str, subject: str, details: dict) -> None:
    """Publish alert notification to SNS topic."""
    sns = get_client("sns")
    message = json.dumps(details, indent=2)
    log.info("Publishing alert to SNS topic %s: %s", topic_arn, subject)
    try:
        sns.publish(TopicArn=topic_arn, Subject=subject, Message=message)
    except Exception as err:
        log.warning("SNS publish call handled: %s", err)


if __name__ == "__main__":
    publish_alert("arn:aws:sns:us-east-1:123:alert", "Data Quality Failure", {"failed_records": 12})
