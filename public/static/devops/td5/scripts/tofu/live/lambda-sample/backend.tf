terraform {
  backend "s3" {
    bucket         = "samba-diallo-devops-tofu-state-2025"
    key            = "td5/tofu/live/lambda-sample"
    region         = "us-east-2"
    encrypt        = true
    dynamodb_table = "samba-diallo-devops-tofu-state-2025"
  }
}