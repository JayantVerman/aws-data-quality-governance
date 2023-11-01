output "raw_bucket_name" {
  description = "S3 raw bucket name."
  value       = module.s3.raw_bucket_id
}

output "raw_bucket_arn" {
  description = "S3 raw bucket ARN."
  value       = module.s3.raw_bucket_arn
}

output "curated_bucket_name" {
  description = "S3 curated bucket name."
  value       = module.s3.curated_bucket_id
}

output "curated_bucket_arn" {
  description = "S3 curated bucket ARN."
  value       = module.s3.curated_bucket_arn
}

output "quarantine_bucket_name" {
  description = "S3 quarantine bucket name."
  value       = module.s3.quarantine_bucket_id
}

output "quarantine_bucket_arn" {
  description = "S3 quarantine bucket ARN."
  value       = module.s3.quarantine_bucket_arn
}

output "glue_database_name" {
  description = "Glue Data Catalog database name."
  value       = module.glue_catalog.database_name
}

output "sns_topic_arn" {
  description = "SNS topic ARN for governance alerts."
  value       = module.sns.topic_arn
}

output "data_processor_role_arn" {
  description = "IAM role ARN assumed by the data-processing runtime."
  value       = module.iam.data_processor_role_arn
}

output "glue_role_arn" {
  description = "IAM role ARN assumed by the Glue Crawler."
  value       = module.iam.glue_role_arn
}

output "lakeformation_role_arn" {
  description = "IAM role ARN for Lake Formation permission delegation."
  value       = module.iam.lakeformation_role_arn
}