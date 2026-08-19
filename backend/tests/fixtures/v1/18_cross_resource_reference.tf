# Resource referencing another resource's attribute across types (S3 bucket referenced
# by a Lambda's environment variable) — tests relationship discovery beyond simple
# security-group/IAM patterns.
resource "aws_s3_bucket" "lambda_data" {
  bucket = "skynex-test-lambda-data"
}

resource "aws_iam_role" "lambda_role" {
  name = "skynex-test-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_lambda_function" "processor" {
  function_name = "skynex-test-processor"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "python3.12"

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.lambda_data.bucket
    }
  }
}
