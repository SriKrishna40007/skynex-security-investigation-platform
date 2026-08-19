# Syntactically valid HCL but not a resource/provider/module block at all
variable "unused_var" {
  type = string
}

locals {
  some_value = "not a resource definition"
}
