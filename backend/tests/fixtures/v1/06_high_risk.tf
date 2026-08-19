# Public S3 bucket + wildcard bucket policy -> expected HIGH severity finding
resource "aws_s3_bucket" "public_bucket" {
  bucket = "skynex-test-public-bucket"
}

resource "aws_s3_bucket_policy" "public_policy" {
  bucket = aws_s3_bucket.public_bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = "*"
      Action    = "s3:*"
      Resource  = "${aws_s3_bucket.public_bucket.arn}/*"
    }]
  })
}
