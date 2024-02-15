"""Unit tests for alert publisher payload formatting."""

import json
from unittest.mock import patch, MagicMock
from alerting.sns_handlers.alert_publisher import publish_alert


@patch("alerting.sns_handlers.alert_publisher.get_client")
def test_publish_alert_dryrun(mock_get_client):
    """Verify publish_alert runs without error in dry-run mode."""
    mock_sns = MagicMock()
    mock_get_client.return_value = mock_sns
    publish_alert("mock-arn", "Test Alert", {"status": "ok"})


@patch("alerting.sns_handlers.alert_publisher.get_client")
def test_publish_alert_calls_sns_publish(mock_get_client):
    """Verify publish_alert calls SNS publish with correct parameters."""
    mock_sns = MagicMock()
    mock_get_client.return_value = mock_sns

    topic_arn = "arn:aws:sns:us-east-1:123456789012:test-topic"
    subject = "Data Quality Failure"
    details = {"failed_records": 12, "quality_score": 85.5}

    publish_alert(topic_arn, subject, details)

    mock_get_client.assert_called_once_with("sns")
    mock_sns.publish.assert_called_once()

    call_args = mock_sns.publish.call_args
    assert call_args[1]["TopicArn"] == topic_arn
    assert call_args[1]["Subject"] == subject

    message = json.loads(call_args[1]["Message"])
    assert message["failed_records"] == 12
    assert message["quality_score"] == 85.5


@patch("alerting.sns_handlers.alert_publisher.get_client")
def test_publish_alert_handles_exception(mock_get_client):
    """Verify publish_alert handles SNS exceptions gracefully."""
    mock_sns = MagicMock()
    mock_sns.publish.side_effect = Exception("SNS service unavailable")
    mock_get_client.return_value = mock_sns

    # Should not raise - exception is logged and swallowed
    publish_alert("mock-arn", "Test", {"data": "value"})

