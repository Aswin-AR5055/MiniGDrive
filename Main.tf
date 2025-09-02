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

data "aws_security_group" "existing_sg" {
  filter {
    name = "group-name"
    values = ["mysecuritygroup_ar"]
  }

}

resource "aws_instance" "my_instance" {
    ami = data.aws_ami.my_ubuntu_ami.id
    instance_type = "t2.micro"
    key_name = "newubuntukeypair"
    vpc_security_group_ids = [data.aws_security_group.existing_sg.id]

    tags = {
      Name = "MiniGDrive_Test_Instance"
    }
}

output "instance_public_ip" {
    value = aws_instance.my_instance.public_ip
}
