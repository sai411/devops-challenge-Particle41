# devops-challenge-Particle41
# SimpleTimeService

Tiny microservice that returns a JSON with timestamp and visitor ip.
This repository contains:

app/ : Python Flask app + Dockerfile (runs as a non-root user)

terraform/ : Terraform code to deploy VPC, ECS (Fargate), and an Application Load Balancer (ALB)

Quick local test (build & run)

Prereqs:

Docker

# Clone the repository
git clone https://github.com/<your-username>/devops-challenge-Particle41.git

# change directory
cd devops-challenge-Particle41/app

# build image
docker build -t simpletimeservice:local .

# run container
docker run --rm -p 8080:8080 simpletimeservice:local

# test locally
curl http://localhost:8080/

To push Docker image to DockerHub
docker tag simpletimeservice:local yourdockerhubuser/simpletimeservice:1.0.0
docker login
docker push yourdockerhubuser/simpletimeservice:1.0.0


This makes the image publicly available to be used in ECS deployments (or Kubernetes, EKS, etc.).

To Deploy the image in AWS

Run the below commands to provision the required infrastructure.

Prereqs:

Terraform >= 1.4
AWS CLI or AWS credentials exported as environment variables
Public Docker image (DockerHub or ECR)

Authentication:

You must configure AWS credentials locally before running Terraform.

Option 1 — Configure using AWS CLI:
aws configure


Then provide:

AWS Access Key ID

AWS Secret Access Key

AWS Region (example: us-east-1)

Option 2 — Configure as environment variables:
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_REGION=us-east-1

Authorization:

Ensure your IAM user/role has permissions for:

VPC

Subnets / Route Tables / NAT / IGW

ECS Cluster

Task Definitions & ECS Service

Load Balancer + Target Groups

CloudWatch Logs

IAM role creation for ECS execution

Terraform backend to store state file (optional)

terraform/backend.tf is included as an example for using:

S3 → store state file

DynamoDB → state locking

You may enable it by updating bucket/table names.

Deploy Terraform Infrastructure
move to correct directory
cd terraform

initialize
terraform init

plan (show changes)
terraform plan -var="app_image=yourdockerhubuser/simpletimeservice:latest"

apply (create infra)
terraform apply -var="app_image=yourdockerhubuser/simpletimeservice:latest" -auto-approve


After apply completes, Terraform prints:

alb_dns_name = "<your-public-alb-dns>"


Open in browser:

http://<alb_dns_name>/


You should see the JSON response from SimpleTimeService.

CI-CD pipeline
Go to the Actions tab and click on "Run workflow".

I have included a workflow_dispatch trigger, so the workflow can be run manually.

(Automatic triggers on push to main are included but commented out. 
You can enable them anytime.)

Note that NO secrets are included in this repository. 
To run the CI/CD pipeline, please fork the repository and add the following secrets 
in your GitHub Actions → Settings → Secrets:

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- DOCKERHUB_USERNAME
- DOCKERHUB_TOKEN


Once added, the pipeline will:

Build the Docker image

Push to DockerHub

Deploy the Terraform infrastructure (optional)
