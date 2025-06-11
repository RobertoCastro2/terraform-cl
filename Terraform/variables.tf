variable "aws_region" {
  description = "Região AWS"
  type        = string
  default     = "us-east-2"
}

variable "network_stack_name" {
  description = "Nome do stack CloudFormation de rede"
  type        = string
  default     = "network-stack"
}

variable "instance_type" {
  description = "Tipo de instância EC2"
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "AMI para a instância EC2"
  type        = string
  default     = "ami-0bdf93799014acdc4"  # troque pelo ID correto
}

variable "key_name" {
  description = "Key Pair para SSH na EC2"
  type        = string
  default     = "minha-chave-ec2"
}