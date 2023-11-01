# Root Terraform configuration for aws-data-quality-governance.
#
# Modules are applied in dependency order:
#   1. iam        — least-privilege roles used by every other module
#   2. s3         — raw + curated buckets (depends on iam)
#   3. glue_catalog — Glue database + crawler (depends on s3)
#   4. sns        — alerting topic (depends on iam)
#   5. lake_formation — LF permissions (depends on s3, glue_catalog, iam)
#
# To apply:
#   cd infra && terraform init && terraform plan && terraform apply
# To destroy (reverse order):
#   cd infra && terraform destroy -auto-approve

terraform {
  required_version = ">= 1.7.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "aws-data-quality-governance"
      ManagedBy   = "terraform"
      Environment = var.environment
    }
  }
}

# --- 1. IAM (no dependencies) ---------------------------------------------

module "iam" {
  source = "./modules/iam"
  project_name = var.project_name
  environment  = var.environment
}

# --- 2. S3 (depends on iam) -----------------------------------------------

module "s3" {
  source       = "./modules/s3"
  project_name = var.project_name
  environment  = var.environment
}

# --- 3. Glue Catalog (depends on s3, iam) ---------------------------------

module "glue_catalog" {
  source       = "./modules/glue_catalog"
  project_name = var.project_name
  environment  = var.environment
  raw_bucket_arns = [
    module.s3.raw_bucket_arn,
    module.s3.curated_bucket_arn,
    module.s3.quarantine_bucket_arn,
  ]
  glue_role_arn = module.iam.glue_role_arn
}

# --- 4. SNS (depends on iam) ----------------------------------------------

module "sns" {
  source       = "./modules/sns"
  project_name = var.project_name
  environment  = var.environment
}

# --- 5. Lake Formation (depends on s3, glue_catalog, iam) ------------------

module "lake_formation" {
  source = "./modules/lake_formation"
  project_name = var.project_name
  environment  = var.environment
  raw_bucket_arns = [
    module.s3.raw_bucket_id,
    module.s3.curated_bucket_id,
    module.s3.quarantine_bucket_id,
  ]
  glue_database_name    = module.glue_catalog.database_name
  glue_catalog_role_arn = module.iam.glue_role_arn
  lakeformation_role_arn = module.iam.lakeformation_role_arn
  data_processor_role_arn = module.iam.data_processor_role_arn
}