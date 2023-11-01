output "data_processor_role_arn" {
  description = "IAM role ARN assumed by the data-processing runtime."
  value       = aws_iam_role.data_processor.arn
}

output "glue_role_arn" {
  description = "IAM role ARN assumed by the Glue Crawler."
  value       = aws_iam_role.glue.arn
}

output "lakeformation_role_arn" {
  description = "IAM role ARN for Lake Formation permission delegation."
  value       = aws_iam_role.lakeformation.arn
}