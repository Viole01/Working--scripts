# Import necesasry modules
import boto3
from datetime import datetime, timedelta

# Create a console session
aws_console = boto3.session.Session(profile_name="default")

# Open the s3 console from the main consile
s3 = aws_console.client(service_name="s3", region_name="us-east-1")

bucket_name = ''

# Setting the current datetime
current_date = datetime.now()

# Setting the 30 days old datetime
threshold_date = current_date - timedelta(days=30)

# Listing all the objects in the bucket
objects = s3.list_objects_v2(Bucket=bucket_name)['Contents']

for obj in objects:
    # Checking if the object is older than 30 days
    last_modified_date = obj['LastModified'].replace(tzinfo=None)
    if last_modified_date < threshold_date:
        # Deleting the object
        s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
        print(f"Deleted {obj['Key']}")

print("All objects older than 30 days have been deleted.")