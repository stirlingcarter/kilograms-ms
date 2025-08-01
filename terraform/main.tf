terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "meilisearch_server" {
  ami           = var.aws_ami
  instance_type = var.instance_type
  key_name      = var.key_name
  security_groups = [aws_security_group.meilisearch_sg.name]

  tags = {
    Name = "MeiliSearch-Server"
  }
}

resource "aws_ebs_volume" "meilisearch_data" {
  availability_zone = aws_instance.meilisearch_server.availability_zone
  size              = var.ebs_volume_size
  type              = "gp2"
  tags = {
    Name = "MeiliSearch-Data"
  }
}

resource "aws_volume_attachment" "ebs_att" {
  device_name = "/dev/sdh"
  volume_id   = aws_ebs_volume.meilisearch_data.id
  instance_id = aws_instance.meilisearch_server.id
}

resource "aws_security_group" "meilisearch_sg" {
  name        = "meilisearch-sg"
  description = "Allow SSH and MeiliSearch traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 7700
    to_port     = 7700
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
} 