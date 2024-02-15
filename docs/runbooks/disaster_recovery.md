# Disaster Recovery Runbook

Steps for recovering from compromised bucket states or catalog corruption.

## Scenarios

### 1. S3 Bucket Data Loss or Corruption

**Symptoms**: Missing or corrupted files in raw, curated, or quarantine buckets.

**Recovery Steps**:

1. **Identify the affected bucket and prefix**:
   ```bash
   aws s3 ls s3://aws-data-quality-governance-dev-raw/raw/
   aws s3 ls s3://aws-data-quality-governance-dev-curated/
   aws s3 ls s3://aws-data-quality-governance-dev-quarantine/
   ```

2. **Regenerate synthetic data** (if raw data is lost):
   ```bash
   ./scripts/seed_data.sh 1000
   ```

3. **Re-run the quality pipeline** (if curated/quarantine data is lost):
   ```bash
   ./scripts/run_pipeline.sh
   ```

4. **Verify data integrity**:
   ```bash
   aws s3 ls s3://aws-data-quality-governance-dev-raw/raw/
   aws s3 ls s3://aws-data-quality-governance-dev-curated/
   ```

### 2. Glue Catalog Corruption

**Symptoms**: Missing tables, incorrect schema, or crawler failures.

**Recovery Steps**:

1. **Delete the corrupted database** (cascade drops all tables):
   ```bash
   aws glue delete-database --name aws_data_quality_governance_dev_customers
   ```

3. **Re-provision via Terraform**:
   ```bash
   cd infra
   terraform apply -target=module.glue_catalog
   ```

4. **Re-run the crawler**:
   ```bash
   aws glue start-crawler --name aws-data-quality-governance-dev-customers-crawler
   ```

5. **Verify catalog restoration**:
   ```bash
   aws glue get-tables --database-name aws_data_quality_governance_dev_customers
   ```

### 3. Lake Formation Permission Issues

**Symptoms**: Users unable to query data, permission denied errors in Athena.

**Recovery Steps**:

1. **Check current permissions**:
   ```bash
   aws lakeformation list-permissions --resource-type TABLE
   ```

2. **Re-apply Lake Formation module**:
   ```bash
   cd infra
   terraform apply -target=module.lake_formation
   ```

3. **Verify with test query**:
   ```bash
   python governance/lake_formation/query_demo.py
   ```

### 4. Complete Infrastructure Loss

**Symptoms**: All AWS resources accidentally deleted.

**Recovery Steps**:

1. **Re-provision all infrastructure**:
   ```bash
   cd infra
   terraform init
   terraform apply -auto-approve
   ```

2. **Re-seed data**:
   ```bash
   ./scripts/seed_data.sh 1000
   ```

3. **Run full pipeline**:
   ```bash
   ./scripts/run_pipeline.sh
   ```

4. **Verify dashboard**:
   ```bash
   docker compose up -d
   streamlit run viz/streamlit_app/app.py
   ```

## Prevention

- Enable S3 Versioning on all buckets (configured in Terraform)
- Enable Glue Catalog backup via AWS Backup
- Store Terraform state in S3 with versioning
- Regularly test recovery procedures

