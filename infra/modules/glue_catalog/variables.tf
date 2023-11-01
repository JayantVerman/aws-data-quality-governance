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
  description = "List of S3 bucket ARNs the crawler may scan."
  type        = list(string)
  default     = []
}

variable "glue_role_arn" {
  description = "IAM role ARN assumed by the Glue Crawler."
  type        = string
}