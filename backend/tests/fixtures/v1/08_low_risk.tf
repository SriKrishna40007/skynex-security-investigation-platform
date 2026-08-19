# SG restricted to internal CIDR only -> expected LOW/no finding
resource "aws_security_group" "low_risk_sg" {
  name        = "skynex-test-low-risk-sg"
  description = "Internal only"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
}
