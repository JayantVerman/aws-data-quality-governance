output "raw_bucket_id" {
  description = "S3 raw bucket ID."
  value       = aws_s3_bucket.raw.id
}

output "curated_bucket_id" {
  description = "S3 curated bucket ID."
  value       = aws_s3_bucket.curated.id
}

output "quarantine_bucket_id" {
  description = "S3 quarantine bucket ID."
  value       = aws_s3_bucket.quarantine.id
}