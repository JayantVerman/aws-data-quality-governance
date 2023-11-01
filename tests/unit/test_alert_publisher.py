"""Unit tests for alert publisher payload formatting."""

from alerting.sns_handlers.alert_publisher import publish_alert


def test_publish_alert_dryrun():
    publish_alert("mock-arn", "Test Alert", {"status": "ok"})
