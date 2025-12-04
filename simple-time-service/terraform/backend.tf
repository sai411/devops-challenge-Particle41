terraform {
  backend "s3" {
    bucket         = "simple-time-service-project"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    use_lockfile   = "true"
  }
}
