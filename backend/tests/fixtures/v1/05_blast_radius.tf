# Central shared IAM role used by three separate resources — compromise of the role
# should have a blast radius covering all three.
resource "aws_iam_role" "shared_role" {
  name = "skynex-test-shared-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_instance_profile" "shared_profile" {
  name = "skynex-test-shared-profile"
  role = aws_iam_role.shared_role.name
}

resource "aws_instance" "server_1" {
  ami                  = "ami-0123456789abcdef0"
  instance_type        = "t3.micro"
  iam_instance_profile = aws_iam_instance_profile.shared_profile.name
}

resource "aws_instance" "server_2" {
  ami                  = "ami-0123456789abcdef0"
  instance_type        = "t3.micro"
  iam_instance_profile = aws_iam_instance_profile.shared_profile.name
}

resource "aws_instance" "server_3" {
  ami                  = "ami-0123456789abcdef0"
  instance_type        = "t3.micro"
  iam_instance_profile = aws_iam_instance_profile.shared_profile.name
}
