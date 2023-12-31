import boto3
from datetime import datetime, timedelta

# Create aws console session
aws_console = boto3.session.Session(profile_name="default")

# Create S3 client
s3 = aws_console.client(service_name="s3", region_name="us-east-1")

# Create Glacier client
glacier = aws_console.client(service_name="glacier", region_name="us-east-1")

# Variables
bucket_name = ''
days_threshold = 180 # 6 months in days
current_date = datetime.now()
threshold_date = current_date - timedelta(days=days_threshold)

# List all Objs in the bucket
response = s3.list_objects_v2(Bucket=bucket_name)

# Checking age of objects
for obj in response['Contents']:
    if obj['LastModified'] > threshold_date:
        # Get the Obj content
        obj_content = s3.get_object(Bucket=bucket_name, Key=obj['Key'])['Body'].read()
        # Move the object to glacier
        archive_response = glacier.upload_archive(
            vaultName='',
            archiveDescription='Object age is more than 6 months',
            body=obj_content,
        )
        print(f"Archive initiated for {obj['Key']}. Archive ID: {archive_response['archiveId']}")