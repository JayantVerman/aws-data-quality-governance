# Lake Formation Governance Module

resource "aws_lakeformation_data_lake_settings" "settings" {
  admins = [var.lakeformation_role_arn]
}

resource "aws_lakeformation_resource" "raw_location" {
  arn = var.raw_bucket_arns[0]
}

resource "aws_lakeformation_lf_tag" "pii_tag" {
  key    = "PII_Level"
  values = ["High", "Low", "None"]
}
