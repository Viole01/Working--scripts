import boto3

# Open a session console
aws_console = boto3.session.Session(profile_name="default")

# Create s3 resource and client
s3_resource = aws_console.resource(service_name='s3')
s3_client = aws_console.client(service_name='s3')

resouurce_response = list(s3_resource.buckets.all())

def check_uncrypted_buckets():
    for bucket in resouurce_response:
        encryption_status = s3_client.get_bucket_encryption(Bucket=bucket.name)
        if not encryption_status.get('ServerSideEncryptionConfiguration'):
            print(f"Bucket {bucket.name} is not encrypted")

check_uncrypted_buckets()