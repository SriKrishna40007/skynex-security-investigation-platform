# Multiple independent, valid resources — no cross-references
resource "aws_s3_bucket" "bucket_a" {
  bucket = "skynex-test-bucket-a"
}

resource "aws_s3_bucket" "bucket_b" {
  bucket = "skynex-test-bucket-b"
}

resource "aws_iam_user" "service_user" {
  name = "skynex-test-service-user"
}

resource "aws_security_group" "web_sg" {
  name        = "skynex-test-web-sg"
  description = "Test security group"
}
