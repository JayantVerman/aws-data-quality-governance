# Macie Cost Optimization Runbook

Best practices for running Macie as an on-demand targeted scan to stay inside free limits.

## Understanding Macie Costs

### Free Tier
- **First 30 days**: Free account-level evaluation with S3 bucket/object evaluation quota
- **After free tier**: Billed per GB of data classified

### Cost Drivers
- **Data volume scanned**: More data = higher cost
- **Frequency**: Recurring jobs accumulate costs quickly
- **Scope**: Scanning entire buckets costs more than targeted prefixes

## Optimization Strategies

### 1. Use One-Time Jobs Only

**Do**:
```python
# trigger_scan.py uses ONE_TIME job type
macie.create_classification_job(
    jobType="ONE_TIME",  # Single scan, no recurring charges
    name=f"pii-scan-{bucket_name}",
    ...
)
```

**Don't**:
```python
# NEVER use SCHEDULED jobs for this project
macie.create_classification_job(
    jobType="SCHEDULED",  # Recurring charges!
    ...
)
```

### 2. Scope to Specific Prefixes

Limit the scan to only the raw data location:
```python
s3JobDefinition={
    "scoping": {
        "includes": {
            "and": [
                {
                    "simpleScopeTerm": {
                        "comparator": "EQ",
                        "key": "S3_BUCKET_NAME",
                        "values": [bucket_name],
                    }
                },
                {
                    "simpleScopeTerm": {
                        "comparator": "STARTS_WITH",
                        "key": "OBJECT_KEY",
                        "values": ["raw/"],  # Only scan raw prefix
                    }
                },
            ]
        }
    }
}
```

### 3. Keep Data Volumes Small

- Generate only the data you need: `--rows 1000` (default)
- Avoid re-running scans on unchanged data
- Delete old scan results when no longer needed

### 4. Monitor Costs

Set up AWS Budgets alerts:
```bash
aws budgets create-budget \
    --budget file://budget.json \
    --notifications-with-subscribers file://notifications.json
```

## Recommended Usage Pattern

1. **Initial setup**: Run one-time scan after seeding data
2. **After data changes**: Run scan only when new data is uploaded
3. **Regular monitoring**: Check Macie findings dashboard in AWS Console
4. **Teardown**: No ongoing costs when not actively scanning

## Cost Estimation

| Scenario | Data Volume | Estimated Cost |
|----------|-------------|----------------|
| Initial scan (1,000 rows) | ~1 MB | $0.00 (free tier) |
| Monthly re-scan | ~1 MB | $0.10 - $0.50 |
| Large dataset (100K rows) | ~100 MB | $1.00 - $5.00 |

*Note: Costs are estimates. Check current Macie pricing for exact rates.*

