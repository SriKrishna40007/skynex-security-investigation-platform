# SG open on a single non-standard port to 0.0.0.0/0 -> expected MEDIUM severity
resource "aws_security_group" "medium_risk_sg" {
  name        = "skynex-test-medium-risk-sg"
  description = "Single port open to internet"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
