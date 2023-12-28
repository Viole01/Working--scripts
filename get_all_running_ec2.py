# Get all Modules & libs
import boto3

# Open AWS management console
aws_management_console = boto3.session.Session(profile_name="default")

# Open EC2 Console
ec2_console = aws_management_console.client(service_name="ec2", region_name="us-east-1")

# Use boto3 Docs for more info (https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
result = ec2_console.describe_instances()["Reservations"][0]['Instances']
for each_instance in result:
    print(each_instance['instanceId'])