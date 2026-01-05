provider "aws" {
  region = "us-east-2"
}

module "state" {
  source = "../../modules/state-bucket"

  name = "samba-diallo-devops-tofu-state-2025"
}