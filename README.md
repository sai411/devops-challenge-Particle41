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
```

# To Deploy the image in the AWS, Run the below commangs for creating the required infrastructure

Authentication:

You must configure AWS credentials locally , there are two ways, one is to add the credentials in providers.tf file and other way is to configure in your local cli and run the terraform commands.

```bash
aws configure
```
Then Provide the values it asked for 

You can also add them as Environment variables, When you were assuming any role, once you added the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY of your IAM user by above command.

export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_REGION=us-east-1

Authorization:

Add required policies/permissions to the above users/role to provide access to provision the resources.


# initialize
```bash
terraform init
```
# plan (show changes)
```
terraform plan -var="app_image=yourdockerhubuser/simpletimeservice:latest"
```

# apply (create infra)
```
terraform apply -var="app_image=yourdockerhubuser/simpletimeservice:latest" -auto-approve
```
