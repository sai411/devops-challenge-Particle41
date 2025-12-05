# devops-challenge-Particle41
# SimpleTimeService

Tiny microservice that returns a JSON with timestamp and visitor ip. The SimpleTimeService application is a lightweight Flask-based API that listens on port 8080 and returns the current timestamp along with the requester’s IP address in JSON format. When a user or client makes an HTTP request to the root endpoint (/), the request is received by the containerized application running inside an ECS Fargate task. The application determines the client IP (direct or forwarded through the load balancer), generates an ISO-formatted timestamp, and returns both values as a simple JSON response. The container runs with Gunicorn in a non-root user context to maintain secure runtime practices while keeping the app minimal and fast.

This repository contains:

app/ : Python Flask app + Dockerfile (runs as a non-root user)

terraform/ : Terraform code to deploy VPC, ECS (Fargate), and an Application Load Balancer (ALB)

- `app/` : Python Flask app + Dockerfile
- `terraform/` : Terraform code to deploy VPC + ECS + ALB

# Quick local test (build & run)
Prereqs:
- Docker

```bash
# Clone
git clone https://github.com/sai411/devops-challenge-Particle41.git

# Change directory
cd devops-challenge-Particle41/simple-time-service/app

# build image
docker build -t simpletimeservice:local .

# run
docker run --rm -p 8080:8080 simpletimeservice:local

# test
curl http://localhost:8080/
```

# Verify the Output
Sample:
```
{
  "ip": "223.185.50.194",
  "timestamp": "2025-12-05T22:43:05.130592+05:30"
}
```

# To push docker image to a repository Dockerhub

```
docker tag simpletimeservice:local yourdockerhubuser/simpletimeservice:1.0.0
docker login
docker push yourdockerhubuser/simpletimeservice:1.0.0
```

Then the image will be available in your remote repository can be used in kubernetes(EKS) or ECS based deployments.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# To provision the infrastructure resources in the AWS, Run the below commands locally after cloning the repo

The infrastructure is designed using AWS best practices to securely host containerized applications. A VPC is created with both public and private subnets so that internet-facing components like the Application Load Balancer operate in public subnets, while the ECS Fargate tasks run in private subnets without direct internet exposure. A NAT Gateway enables the tasks to securely pull images from DockerHub or ECR. The ALB receives incoming traffic, forwards it to the ECS service registered under a target group, and performs health checks to ensure availability. ECS Fargate is used to remove the need for managing EC2 nodes and to automatically scale and secure the workload. CloudWatch Logs capture container logs, IAM roles secure the task execution. I have used wait_for_steady_state = true in the ECS terraform configuration as the execution will wait until ECS service was active with desired tasks running.

Prereqs:

```text
Terraform >= 1.4

AWS CLI or AWS credentials (via env vars or profile or IAM role) as mentioned below

Docker image available publicly (DockerHub or ECR)
```

# Authentication:

You must configure AWS credentials locally , there are two ways, one is to add the credentials in providers.tf file and other way is to configure in your local cli and run the terraform commands.

```bash
aws configure
```
Then provide the values it asks for

```
AWS Access Key ID

AWS Secret Access Key

AWS Region (example: us-east-1)
```

You can also add them as Environment variables, to use the IAM user

export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_REGION=us-east-1. 

If you would like to use IAM role, you need to add the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and aws_session_token of your IAM role, only after adding the user details.

# Authorization:

```
Add required policies/permissions to the above users/role to provide access to provision the resources.

Ensure your IAM user/role has permissions for:

VPC
Subnets/Route Tables/NAT/IGW
ECS Cluster
Task Definitions & ECS Service
Load Balancer + Target Groups
CloudWatch Logs
IAM role creation for ECS execution
```

# Terraform backend to store state file:

terraform/backend.tf included for S3 which has lock file mechanism and can be used for storing the statefile.I have used an s3 bucket with name: simple-time-service-project , if you want to continue with the script , please create an S3 buvket in your AWS account as well, or else update the s3 name name in terraform/backend.tf 

# Follow the steps below to run and provision the resources and finally deploy the application in ECS by using below commands

# move to correct directory
```
cd devops-challenge-Particle41/simple-time-service/terraform
```

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

After apply completes, Terraform prints alb_dns_name. Open http://<alb_dns_name>/

# CI-CD pipeline:

This pipeline consists of two jobs, one is the CI job which performs cloning to docker build and push to repository. And the other one is the Terraform job which will provision the required resources and deploy the generated image in the ECS cluster.

```
Go to the Actions tab and click on "Run workflow".

I have included a workflow_dispatch trigger, so the workflow can be run manually. (Automatic triggers on push to main are included but commented out.
You can enable them anytime.)

Note that NO secrets are included in this repository.
To run the CI/CD pipeline, please fork the repository and add the following secrets
in your GitHub Actions → Settings → Secrets:

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- DOCKERHUB_USERNAME
- DOCKERHUB_TOKEN


```

Once added, the pipeline will:

1. Build the Docker image (as a build_number tag, example image DockerUserName/simpletimeservice:<build-number>)

2. Push to DockerHub

3. Deploy the Terraform infrastructure
