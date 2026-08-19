# Fully locked-down, least-privilege configuration -> expect zero findings
resource "aws_iam_role" "least_priv_role" {
  name = "skynex-test-least-priv-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "least_priv_policy" {
  name = "skynex-test-least-priv-policy"
  role = aws_iam_role.least_priv_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject"]
      Resource = "arn:aws:s3:::skynex-test-specific-bucket/readonly/*"
    }]
  })
}
