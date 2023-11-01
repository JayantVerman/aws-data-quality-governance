# S3 module — three buckets:
#   - raw:        landing zone for generated synthetic data
#   - curated:    output of the quality transform (approved rows)
#   - quarantine: failed rows routed here by Great Expectations
#
# All three use SSE-S256 encryption and block public access by default.

locals {
  base_name = "${var.project_name}-${var.environment}"
}

resource "aws_s3_bucket" "raw" {
  bucket = "${local.base_name}-raw"
}

resource "aws_s3_bucket" "curated" {
  bucket = "${local.base_name}-curated"
}

resource "aws_s3_bucket" "quarantine" {
  bucket = "${local.base_name}-quarantine"
}

resource "aws_s3_bucket_server_side_configuration" "raw" {
  bucket = aws_s3_bucket.raw.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_server_side_configuration" "curated" {
  bucket = aws_s3_bucket.curated.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_server_side_configuration" "quarantine" {
  bucket = aws_s3_bucket.quarantine.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "raw" {
  bucket                  = aws_s3_bucket.raw.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "curated" {
  bucket                  = aws_s3_bucket.curated.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "quarantine" {
  bucket                  = aws_s3_bucket.quarantine.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}