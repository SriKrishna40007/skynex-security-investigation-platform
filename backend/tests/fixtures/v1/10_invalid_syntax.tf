# Deliberately malformed HCL — unclosed block, missing quote
resource "aws_s3_bucket" "broken_bucket {
  bucket = skynex-test-broken
