# Minimal valid Terraform: single S3 bucket, no relationships, no findings expected
resource "aws_s3_bucket" "minimal_bucket" {
  bucket = "skynex-test-minimal-bucket"
}
