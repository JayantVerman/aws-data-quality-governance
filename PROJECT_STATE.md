# Project State — aws-data-quality-governance

## Current Phase
Phase 0: Scaffolding — Status: done

## Completed Phases (collapsed summary)
- Phase 0: Repo skeleton scaffolded — done

## File Manifest
- data_generator/generate_synthetic_pii.py — Faker-based generator, outputs CSV to data/synthetic/
- orchestration/airflow/dags/ — Airflow DAGs driving the pipeline
- infra/ — Terraform modules for S3, Glue, Lake Formation, SNS, IAM
- governance/macie/ — Macie scan trigger + findings parser
- governance/lake_formation/ — LF permission definitions
- data_quality/great_expectations/ — GE suites
- lineage/openlineage_config/ — OpenLineage + Marquez config
- alerting/sns_handlers/ — SNS alerting
- viz/streamlit_app/ — Streamlit dashboard
- tests/ — unit + integration tests
- scripts/ — setup.sh, seed_data.sh, teardown.sh
- docs/ — diagrams + runbooks

## Open Decisions / Blockers
- Awaiting user confirmation before Phase 2 (real AWS resources).

## Next Actions (top 3)
1. Confirm AWS credentials and readiness to incur minimal cost.
2. Execute Phase 2 — AWS foundation (S3, IAM, Glue).
3. Continue through Phases 3–11.

## Deviations from Locked Architecture
- <none yet>

## AWS Cost Log (running total of what's been deployed/torn down)
- <none yet>