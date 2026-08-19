terraform {
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = "ap-southeast-2"
}

resource "aws_vpc" "production" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name        = "skynex-production"
    Environment = "production"
  }
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.production.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "skynex-public"
  }
}

resource "aws_security_group" "web" {
  name   = "skynex-web"
  vpc_id = aws_vpc.production.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web" {
  ami           = "ami-demo"
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public.id

  vpc_security_group_ids = [
    aws_security_group.web.id
  ]

  tags = {
    Name        = "skynex-web"
    Environment = "production"
  }
}
