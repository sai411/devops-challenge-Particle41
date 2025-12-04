# devops-challenge-Particle41
# SimpleTimeService

Tiny microservice that returns a JSON with `timestamp` and visitor `ip`.
This repository contains:

- `app/` : Python Flask app + Dockerfile
- `terraform/` : Terraform code to deploy VPC + ECS + ALB

# Quick local test (build & run)
Prereqs:
- Docker

```bash
# Clone
git clone

# change directory
cd devops-challenge-Particle41/app

# build image
docker build -t simpletimeservice:local .

# run
docker run --rm -p 8080:8080 simpletimeservice:latest

# test
curl http://localhost:8080/

# To Deploy the image in the AWS, Run the below commangs for creating the required infrastructure

# initialize
terraform init

# plan (show changes)
terraform plan -var="app_image=yourdockerhubuser/simpletimeservice:latest"

# apply (create infra)
terraform apply -var="app_image=yourdockerhubuser/simpletimeservice:latest" -auto-approve
