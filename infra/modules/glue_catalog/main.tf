# Glue Catalog module — database + crawler for the synthetic dataset.
#
# The crawler infers the schema from the CSV in S3 raw and writes it
# into the Glue Data Catalog. Downstream consumers (Athena, Lake
# Formation, Great Expectations) read from this catalog.

locals {
  base_name = "${var.project_name}-${var.environment}"
}

resource "aws_glue_catalog_database" "customers" {
  name = "${local.base_name}_customers"
  description = "Synthetic customer dataset with PII fields."

  catalog_id = data.aws_caller_identity.current.account_id
}

resource "aws_glue_crawler" "customers" {
  name        = "${local.base_name}-customers-crawler"
  database    = aws_glue_catalog_database.customers.name
  role        = var.glue_role_arn
  description = "Crawls the raw bucket to populate the Glue Data Catalog."

  s3_target {
    path = "${var.raw_bucket_arns[0]}/raw/"
  }

  schedule = "cron(0 9 * * ? *)"

  classifiers = ["CSV"]
}

output "database_name" {
  description = "Glue Data Catalog database name."
  value       = aws_glue_catalog_database.customers.name
}