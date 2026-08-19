# Larger fixture: 10 EC2 instances behind a shared SG and shared IAM role, to exercise
# blast-radius/stability handling at a "reasonably large" but not pathological scale.
resource "aws_security_group" "fleet_sg" {
  name        = "skynex-test-fleet-sg"
  description = "Shared SG for instance fleet"
  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    cidr_blocks     = ["10.0.0.0/8"]
  }
}

resource "aws_iam_role" "fleet_role" {
  name = "skynex-test-fleet-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_instance_profile" "fleet_profile" {
  name = "skynex-test-fleet-profile"
  role = aws_iam_role.fleet_role.name
}

resource "aws_instance" "fleet" {
  count                  = 10
  ami                    = "ami-0123456789abcdef0"
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.fleet_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.fleet_profile.name
}
