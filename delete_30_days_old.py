import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Replace 'your_bucket_name' with the actual name of your S3 bucket
    bucket_name = 'your_bucket_name'

    # Create an S3 client
    s3 = boto3.client('s3')

    # Get the current date and time
    current_date = datetime.now()

    # Define the threshold for deletion (30 days ago)
    threshold_date = current_date - timedelta(days=30)

    # List objects in the S3 bucket
    objects = s3.list_objects_v2(Bucket=bucket_name)['Contents']

    # Iterate through the objects and delete those older than 30 days
    for obj in objects:
        last_modified_date = obj['LastModified'].replace(tzinfo=None)
        if last_modified_date < threshold_date:
            # Delete the object
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
            print(f"Deleted: {obj['Key']}")

    print("Deletion complete.")

    return {
        'statusCode': 200,
        'body': 'Deletion complete.'
    }
