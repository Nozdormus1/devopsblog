variable "main_bucket_name" {}
variable "environment" {}
variable "region" {}

terraform {
  backend "s3" {}
}

provider "aws" {
  region                  = "${var.region}"
  profile                 = "devops"
}

resource "aws_s3_bucket" "remote_states_tf_bucket" {
  bucket = "${var.main_bucket_name}"
  acl    = "private"

  tags {
    Environment = "${var.environment}"
  }
}
