variable "project_name" {
   description = "Aiven console project name"
   type        = string
   default = "aiven-connection"
}

variable "aws_region" {
    description = "Region in which AWS resources will be deployed"
    type = string
    default = "us-east-1"
}

variable "vpc_cidr" {
    description = "CIDR block for the VPC"
    type = string
}

variable "vpc_public_subnets_cidr" {
    description = "CIDR block for the Public Subnets"
    type = list
}

variable "vpc_private_subnets_cidr" {
    description = "CIDR block for the Private Subnets"
    type = list
}