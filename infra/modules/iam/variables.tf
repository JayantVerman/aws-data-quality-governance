variable "project_name" {
  description = "Project name for resource naming."
  type        = string
}

variable "environment" {
  description = "Deployment environment tag."
  type        = string
  default     = "dev"
}

variable "raw_bucket_arns" {
  description = "List of S3 bucket ARNs the role may list."
  type        = list(string)
  default     = []
}

variable "curated_and_quarantine_object_arns" {
  description = "List of S3 object ARNs for curated and quarantine buckets."
  type        = list(string)
  default     = []
}

variable "glue_database_arn" {
  description = "Glue Data Catalog database ARN."
  type        = string
  default     = ""
}