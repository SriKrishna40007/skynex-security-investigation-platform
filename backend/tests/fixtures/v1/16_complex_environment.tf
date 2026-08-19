# Larger, realistic multi-tier environment: web tier, app tier, data tier, shared IAM,
# and one deliberate misconfiguration for the E2E acceptance walkthrough to surface.
resource "aws_security_group" "web_sg" {
  name        = "skynex-test-complex-web-sg"
  description = "Web tier"
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "app_sg" {
  name        = "skynex-test-complex-app-sg"
  description = "App tier, internal only"
  ingress {
    from_port       = 8443
    to_port         = 8443
    protocol        = "tcp"
    security_groups = [aws_security_group.web_sg.id]
  }
}

resource "aws_security_group" "db_sg" {
  name        = "skynex-test-complex-db-sg"
  description = "Data tier"
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app_sg.id]
  }
}

resource "aws_iam_role" "app_role" {
  name = "skynex-test-complex-app-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

# Deliberate misconfiguration: overly broad S3 permission attached to app role
resource "aws_iam_role_policy" "app_policy" {
  name = "skynex-test-complex-app-policy"
  role = aws_iam_role.app_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "s3:*"
      Resource = "*"
    }]
  })
}

resource "aws_iam_instance_profile" "app_profile" {
  name = "skynex-test-complex-app-profile"
  role = aws_iam_role.app_role.name
}

resource "aws_instance" "web_server" {
  ami                    = "ami-0123456789abcdef0"
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.web_sg.id]
}

resource "aws_instance" "app_server" {
  ami                    = "ami-0123456789abcdef0"
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.app_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.app_profile.name
}

resource "aws_db_instance" "primary_db" {
  identifier             = "skynex-test-complex-db"
  engine                 = "postgres"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  vpc_security_group_ids = [aws_security_group.db_sg.id]
}

resource "aws_s3_bucket" "app_data" {
  bucket = "skynex-test-complex-app-data"
}
