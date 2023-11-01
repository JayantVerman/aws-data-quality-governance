# IAM module — least-privilege roles for the data pipeline.
#
# Three roles:
#   - data_processor_role: assumed by MWAA / Airflow workers; reads raw, writes curated/quarantine
#   - glue_role:           assumed by the Glue Crawler
#   - lakeformation_role:  assumed by Lake Formation for permission delegation
#
# No inline policies that duplicate managed ones; everything is scoped
# to the specific buckets/databases the role actually needs.

locals {
  base_name = "${var.project_name}-${var.environment}"
}

# --- Data processor role ---------------------------------------------------

resource "aws_iam_role" "data_processor" {
  name = "${local.base_name}-data-processor"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowMWAAAssume"
        Effect = "Allow"
        Principal = {
          Service = "airflow-mwaa.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      },
    ]
  })
}

resource "aws_iam_role_policy" "data_processor_s3" {
  name = "${local.base_name}-s3-access"
  role = aws_iam_role.data_processor.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ListRawBucket"
        Effect = "Allow"
        Action = ["s3:ListBucket"]
        Resource = concat(
          var.raw_bucket_arns,
          [for arn in var.raw_bucket_arns : "${arn}/*"]
        )
      },
      {
        Sid    = "ReadWriteCuratedQuarantine"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
        ]
        Resource = var.curated_and_quarantine_object_arns
      },
    ]
  })
}

# --- Glue role -------------------------------------------------------------

resource "aws_iam_role" "glue" {
  name = "${local.base_name}-glue-crawler"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowGlueAssume"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      },
    ]
  })
}

resource "aws_iam_role_policy" "glue_catalog" {
  name = "${local.base_name}-glue-policy"
  role = aws_iam_role.glue.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "GlueCatalogRW"
        Effect = "Allow"
        Action = [
          "glue:CreateDatabase",
          "glue:GetDatabase",
          "glue:GetDatabases",
          "glue:UpdateDatabase",
          "glue:DeleteDatabase",
          "glue:CreateTable",
          "glue:GetTable",
          "glue:GetTables",
          "glue:UpdateTable",
          "glue:DeleteTable",
          "glue:BatchCreatePartition",
          "glue:BatchDeletePartition",
          "glue:GetPartition",
          "glue:GetPartitions",
        ]
        Resource = [
          "*",
        ]
      },
      {
        Sid    = "S3CrawlerAccess"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket",
        ]
        Resource = concat(
          var.raw_bucket_arns,
          [for arn in var.raw_bucket_arns : "${arn}/*"]
        )
      },
    ]
  })
}

# --- Lake Formation role ----------------------------------------------------

resource "aws_iam_role" "lakeformation" {
  name = "${local.base_name}-lakeformation"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowLFAssume"
        Effect = "Allow"
        Principal = {
          Service = "lakeformation.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      },
    ]
  })
}

resource "aws_iam_role_policy" "lakeformation" {
  name = "${local.base_name}-lf-policy"
  role = aws_iam_role.lakeformation.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "LFCatalogPermissions"
        Effect = "Allow"
        Action = [
          "lakeformation:GetDataAccess",
          "lakeformation:GrantPermissions",
          "lakeformation:RevokePermissions",
          "lakeformation:PutDataAccess",
          "lakeformation:GetPermissions",
          "lakeformation:ListPermissions",
          "lakeformation:SearchTablesByLFTags",
          "lakeformation:GetTable",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "S3LFDataAccess"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket",
        ]
        Resource = concat(
          var.raw_bucket_arns,
          [for arn in var.raw_bucket_arns : "${arn}/*"]
        )
      },
    ]
  })
}