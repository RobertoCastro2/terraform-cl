terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_cloudformation_stack" "network" {
  name = var.network_stack_name
}

data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# IAM Role e Instance Profile para permitir pull no ECR
resource "aws_iam_role" "ec2_ecr_role" {
  name               = "ec2-ecr-role"
  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "ec2.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "ec2_ecr_attach" {
  role       = aws_iam_role.ec2_ecr_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_instance_profile" "ec2_ecr_profile" {
  name = "ec2-ecr-profile"
  role = aws_iam_role.ec2_ecr_role.name
}

resource "aws_instance" "app_server" {
  ami                    = data.aws_ami.amazon_linux_2.id
  instance_type          = var.instance_type
  subnet_id              = data.aws_cloudformation_stack.network.outputs["PublicSubnet1Id"]
  vpc_security_group_ids = [data.aws_cloudformation_stack.network.outputs["InstanceSecurityGroupId"]]

  key_name               = var.key_name
  iam_instance_profile   = aws_iam_instance_profile.ec2_ecr_profile.name

  user_data = <<-EOF
    #!/bin/bash
    set -eux

    # Atualiza sistema e instala Docker
    yum update -y
    amazon-linux-extras install docker -y
    systemctl enable --now docker

    # Instala AWS CLI v2
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
    yum install -y unzip
    unzip /tmp/awscliv2.zip -d /tmp
    /tmp/aws/install

    # Autentica no ECR e faz pull das imagens
    aws ecr get-login-password --region ${var.aws_region} \
      | docker login --username AWS --password-stdin 653447836976.dkr.ecr.${var.aws_region}.amazonaws.com

    # Executa serviços gRPC em containers
    docker run -d --name sensor_service   -p 50051:50051 653447836976.dkr.ecr.${var.aws_region}.amazonaws.com/sensor-service:latest
    docker run -d --name processor_service -p 50052:50052 653447836976.dkr.ecr.${var.aws_region}.amazonaws.com/processor-service:latest
    docker run -d --name actuator_service  -p 50053:50053 653447836976.dkr.ecr.${var.aws_region}.amazonaws.com/actuator-service:latest
  EOF

  tags = {
    Name = "app-server"
  }
}
