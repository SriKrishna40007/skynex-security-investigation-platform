# Deliberately over-permissive chain: public-facing SG -> EC2 -> IAM role with
# wildcard policy -> S3 bucket. Expected: attack path from internet to bucket data.
resource "aws_security_group" "public_sg" {
  name        = "skynex-test-public-sg"
  description = "Overly permissive public ingress"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "overprivileged_role" {
  name = "skynex-test-overprivileged-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "wildcard_policy" {
  name = "skynex-test-wildcard-policy"
  role = aws_iam_role.overprivileged_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}

resource "aws_iam_instance_profile" "vuln_profile" {
  name = "skynex-test-vuln-profile"
  role = aws_iam_role.overprivileged_role.name
}

resource "aws_instance" "public_server" {
  ami                    = "ami-0123456789abcdef0"
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.public_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.vuln_profile.name
}

resource "aws_s3_bucket" "sensitive_data" {
  bucket = "skynex-test-sensitive-data"
}
