provider "aws"{
region="ap-south-1"
}
data "aws_ami" "ubuntu_ami"{
most_recent=true
filter {
name="name"
values=["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
}
filter{
name="virtualization-type"
values=["hvm"]
}
owners=["099720109477"]
}
data "aws_security_group" "default" {
    name = "default"
}
resource "aws_instance" "myinstance"{
ami=data.aws_ami.ubuntu_ami.id
instance_type="t2.micro"
key_name=""    #enter your keyname
vpc_security_group_ids = [data.aws_security_group.default.id]
tags={
Name="myinstance"
}
}
output "public_ip"{
value=aws_instance.myinstance.public_ip
}

