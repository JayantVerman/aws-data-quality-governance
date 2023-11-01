# Platform Architecture — aws-data-quality-governance

## Architecture Overview

```mermaid
graph LR
    GEN[Faker Generator] --> S3RAW[S3 Raw Bucket]
    S3RAW --> CRAWL[Glue Crawler]
    CRAWL --> CAT[Glue Data Catalog]
    CAT --> GE[Great Expectations]
    GE -- Pass --> S3CUR[S3 Curated]
    GE -- Fail --> QUAR[S3 Quarantine]
    S3RAW --> MACIE[AWS Macie]
    MACIE --> LF[AWS Lake Formation]
    LF --> ATHENA[Amazon Athena]
    GE -. Alert .-> SNS[Amazon SNS]
    MACIE -. Alert .-> SNS
    GE -. Lineage .-> OL[OpenLineage / Marquez]
    OL --> ST[Streamlit Dashboard]
```

## Core Governance Components
- **Data Generator**: Faker synthetic PII generator
- **Data Catalog**: AWS Glue Crawler + Database
- **Data Quality**: Great Expectations checkpoint runner
- **PII Detection**: AWS Macie on-demand classification
- **Access Governance**: AWS Lake Formation column masking & row-level tags
- **Alerting**: Amazon SNS + Slack Lambda handler
- **Lineage**: OpenLineage + Marquez local container
- **Orchestration**: Apache Airflow DAG
- **Visualization**: Streamlit 5-tab governance dashboard
