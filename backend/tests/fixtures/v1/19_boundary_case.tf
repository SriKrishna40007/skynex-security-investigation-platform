# Boundary case: single resource with the maximum-length name Terraform/AWS allows,
# and a security group with zero ingress/egress rules defined (edge case for engines
# that assume at least one rule exists).
resource "aws_s3_bucket" "boundary_name_test_bucket_with_a_very_long_name_near_limit" {
  bucket = "skynex-test-boundary-case-very-long-bucket-name-example"
}

resource "aws_security_group" "no_rules_sg" {
  name        = "skynex-test-no-rules-sg"
  description = "No ingress or egress rules defined at all"
}
