# FRAMEWORK BLOCK, PLEASE DON'T DELETE
variable "username" {}
variable "environment" {}
variable "region" {}

terraform {
  backend "s3" {}
}
######################################
