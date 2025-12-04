variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "name_prefix" {
  description = "Name prefix for resources"
  type        = string
  default     = "simpletime"
}

variable "app_image" {
  description = "Container image to run (public DockerHub or ECR)"
  type        = string
  default     = "yourdockerhubuser/simpletimeservice:1.0.0"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}
