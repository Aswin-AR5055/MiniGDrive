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

resource "tls_private_key" "privatekey" {
    algorithm = "RSA"
    rsa_bits = 4096
}

resource "local_file" "my_private_key" {
    content = tls_private_key.privatekey.private_key_pem
    filename = "newubuntukeypair.pem"
}

resource "aws_key_pair" "myubuntukey" {
    key_name = "newubuntukeypair"
    public_key = tls_private_key.privatekey.public_key_openssh
}

resource "aws_security_group" "my_sg" {
    name = "mysecuritygroup"
    description = "Allow http and ssh traffic" 
    ingress { 
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress { 
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_instance" "my_instance" {
    ami = data.aws_ami.my_ubuntu_ami.id
    instance_type = "t2.micro"
    key_name = aws_key_pair.myubuntukey.key_name
    vpc_security_group_ids = [aws_security_group.my_sg.id] 
}

output "instance_public_ip" {
    value = aws_instance.my_instance.public_ip
}
