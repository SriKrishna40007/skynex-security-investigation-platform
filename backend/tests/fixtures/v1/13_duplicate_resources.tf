# Two resource blocks with the identical type+name — invalid Terraform, must be
# rejected/flagged, not silently deduplicated or silently accepted twice
resource "aws_s3_bucket" "dup_bucket" {
  bucket = "skynex-test-dup-1"
}

resource "aws_s3_bucket" "dup_bucket" {
  bucket = "skynex-test-dup-2"
}
