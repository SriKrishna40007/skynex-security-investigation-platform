# EC2 instance referencing a security group and an IAM instance profile — creates
# discoverable relationships between resources
resource "aws_security_group" "app_sg" {
  name        = "skynex-test-app-sg"
  description = "App tier security group"
}

resource "aws_iam_role" "app_role" {
  name = "skynex-test-app-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_instance_profile" "app_profile" {
  name = "skynex-test-app-profile"
  role = aws_iam_role.app_role.name
}

resource "aws_instance" "app_server" {
  ami                    = "ami-0123456789abcdef0"
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.app_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.app_profile.name
}
