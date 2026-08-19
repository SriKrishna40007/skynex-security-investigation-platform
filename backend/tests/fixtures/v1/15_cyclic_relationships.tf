# Two security groups referencing each other's ID in ingress rules — creates a cycle
# in the relationship graph. Traversal engine must terminate, not infinite-loop.
resource "aws_security_group" "cycle_a" {
  name        = "skynex-test-cycle-a"
  description = "References cycle_b"
}

resource "aws_security_group" "cycle_b" {
  name        = "skynex-test-cycle-b"
  description = "References cycle_a"
}

resource "aws_security_group_rule" "a_from_b" {
  type                     = "ingress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  security_group_id        = aws_security_group.cycle_a.id
  source_security_group_id = aws_security_group.cycle_b.id
}

resource "aws_security_group_rule" "b_from_a" {
  type                     = "ingress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  security_group_id        = aws_security_group.cycle_b.id
  source_security_group_id = aws_security_group.cycle_a.id
}
