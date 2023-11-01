variable "project_name" { type = string }
variable "environment" { type = string, default = "dev" }
variable "raw_bucket_arns" { type = list(string) }
variable "glue_database_name" { type = string }
variable "glue_catalog_role_arn" { type = string }
variable "lakeformation_role_arn" { type = string }
variable "data_processor_role_arn" { type = string }
