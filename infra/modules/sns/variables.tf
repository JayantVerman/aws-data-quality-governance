variable "project_name" {
  description = "Project name for resource naming."
  type        = string
}

variable "environment" {
  description = "Deployment environment tag."
  type        = string
  default     = "dev"
}

variable "email_subscribers" {
  description = "List of email addresses to subscribe to the alert topic."
  type        = list(string)
  default     = []
}