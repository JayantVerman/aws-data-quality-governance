"""Centralized Configuration Management."""

from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    environment: str = os.getenv("ENVIRONMENT", "dev")
    project_name: str = os.getenv("PROJECT_NAME", "aws-data-quality-governance")
    raw_bucket: str = os.getenv("RAW_S3_BUCKET", "aws-data-quality-governance-dev-raw")
    curated_bucket: str = os.getenv("CURATED_S3_BUCKET", "aws-data-quality-governance-dev-curated")
    quarantine_bucket: str = os.getenv("QUARANTINE_S3_BUCKET", "aws-data-quality-governance-dev-quarantine")
    glue_db_name: str = os.getenv("GLUE_DATABASE_NAME", "aws_data_quality_governance_dev_customers")
    sns_topic_arn: str = os.getenv("SNS_TOPIC_ARN", "")
    marquez_url: str = os.getenv("MARQUEZ_URL", "http://localhost:8080")


settings = Settings()
