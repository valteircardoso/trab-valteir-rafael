resource "aws_s3_bucket" "vr" {
  bucket = "trab-valteir-rafael-${terraform.workspace}"
  acl    = "private"

  tags = {
    Name        = "trab-valteir-rafael-${terraform.workspace}"
    Environment = "admin"
  }
}