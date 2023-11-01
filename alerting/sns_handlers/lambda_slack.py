"""AWS Lambda Handler: Route SNS Alerts to Slack Webhook."""

from __future__ import annotations

import json
import os
import urllib.request


def lambda_handler(event: dict, context: dict) -> dict:
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "")
    for record in event.get("Records", []):
        sns_msg = record.get("Sns", {}).get("Message", "")
        payload = {"text": f"🚨 *AWS Governance Alert*: {sns_msg}"}
        if webhook_url:
            req = urllib.request.Request(
                webhook_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            urllib.request.urlopen(req)
    return {"statusCode": 200, "body": "OK"}
