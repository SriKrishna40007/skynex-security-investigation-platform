# Finding with a clear, well-known remediation: SG with SSH open to the world
resource "aws_security_group" "ssh_open_sg" {
  name        = "skynex-test-remediation-ssh-sg"
  description = "SSH open to internet — should trigger remediation suggestion"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
