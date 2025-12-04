# devops-challenge-Particle41
# SimpleTimeService

Tiny microservice that returns a JSON with timestamp and visitor ip.
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

# To push docker image to a repository Dockerhub

```
docker tag simpletimeservice:local yourdockerhubuser/simpletimeservice:1.0.0
docker login
docker push yourdockerhubuser/simpletimeservice:1.0.0
```

Then the image will be available in your remote repository can be used in kubernetes(EKS) or ECS based deployments.

# To provision the infrastructure resources in the AWS, Run the below commands locally once the repo was cloned

Prereqs:

```text
Terraform >= 1.4

AWS CLI or AWS credentials (via env vars or profile or IAM role) which mentioned below

Docker image available publicly (DockerHub or ECR)
```

Authentication:

You must configure AWS credentials locally , there are two ways, one is to add the credentials in providers.tf file and other way is to configure in your local cli and run the terraform commands.

```bash
aws configure
```
Then Provide the values it asked for 

```
AWS Access Key ID

AWS Secret Access Key

AWS Region (example: us-east-1)
```

You can also add them as Environment variables, When you were assuming any role, once you added the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY of your IAM user by above command.

export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_REGION=us-east-1

Authorization:

Add required policies/permissions to the above users/role to provide access to provision the resources.

Ensure your IAM user/role has permissions for:

VPC
Subnets/Route Tables/NAT/IGW
ECS Cluster
Task Definitions & ECS Service
Load Balancer + Target Groups
CloudWatch Logs
IAM role creation for ECS execution

Terraform backend to store state file:

terraform/backend.tf example included for S3 which has lock file mechanisim anf can be used for storing the sttefile.

# move to correct directory
```
cd terraform
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

This pipeline will consists of two jobs, one is the CI job which performs cloning to docker build and push to repository. And the other one is terraform job which will provision the required resources and deploy the generated image in the ECS cluster.

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

1. Build the Docker image

2. Push to DockerHub

3. Deploy the Terraform infrastructure
