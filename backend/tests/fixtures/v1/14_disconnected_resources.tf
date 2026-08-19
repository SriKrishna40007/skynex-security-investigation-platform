# Multiple resources with zero relationships to each other — relationship engine
# must not invent edges between unrelated resources
resource "aws_s3_bucket" "island_a" {
  bucket = "skynex-test-island-a"
}

resource "aws_iam_user" "island_b" {
  name = "skynex-test-island-b"
}

resource "aws_security_group" "island_c" {
  name        = "skynex-test-island-c"
  description = "Not attached to anything"
}
