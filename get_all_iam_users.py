# Import all modules OR libs
import boto3

# Accessing the management console programatically
aws_management_console = boto3.session.Session(profile_name="boto3")

# Open IAM Console
iam_console_resource  = aws_management_console.resource(service_name="iam")
iam_console_client = aws_management_console.client(service_name="iam")

# IAM list with resource object
for each_user in iam_console_resource.users.all():
    print(each_user.name)

# IAM list with client object
for each_user in iam_console_client.list_users()["Users"]:
    print(each_user["UserName"])
