provider "aws" {
    region = "ap-south-1"
}

data "aws_ami" "my_ubuntu_ami" {
    most_recent = true
    filter {
        name = "name"
        values = ["ubuntu/images/hvm-ssd/ubuntu-*-20.04-amd64-server-*"]
    }
    filter {
        name = "virtualization-type"
        values = ["hvm"]
    }
    owners = ["099720109477"]
}

resource "aws_security_group" "my_sg_new_2" {
  name        = "mysecuritygroup_new_2"
  description = "Allow HTTP and SSH inbound; all outbound"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 8000
    to_port = 8000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "my_instance" {
    ami = data.aws_ami.my_ubuntu_ami.id
    instance_type = "t2.micro"
    key_name = "newubuntukeypair"
    vpc_security_group_ids = [aws_security_group.my_sg_new_2.id]
    tags = {
    Name = "ERDiagramGeneratorserver"
    }
}

output "instance_public_ip" {
    value = aws_instance.my_instance.public_ip
}
