variable "main_bucket_name" {}

resource "aws_s3_bucket" "remote_states_tf_bucket" {
  bucket = "${var.username}-${var.main_bucket_name}"
  acl    = "private"

  tags {
    Environment = "${var.environment}"
  }
}
