# FRAMEWORK BLOCK, PLEASE DON'T DELETE
variable "username" {}
variable "environment" {}
variable "region" {}
######################################

variable "main_bucket_name" {}

terraform {
  backend "s3" {}
}

provider "aws" {
  region                  = "${var.region}"
  profile                 = "devops"
}

resource "aws_s3_bucket" "remote_states_tf_bucket" {
  bucket = "${var.username}-${var.main_bucket_name}"
  acl    = "private"

  tags {
    Environment = "${var.environment}"
  }
}
