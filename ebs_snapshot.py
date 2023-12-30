import boto3
from datetime import datetime, timedelta

# Create an AWS session
aws_console = boto3.session.Session(profile_name="default")

# Create an ec2 session
ec2 = aws_console.client(service_name="ec2", region_name="us-east-1")

# Define variables
volume_id = ''
retention_period = 7 # Time in Days

# Function to create new snapshot of the volume
def create_ebs_snapshot():
    snapshot = ec2.create_snapshot(
        VolumeId=volume_id,
        Description='Created by Prajjwal'
    )
    print(snapshot['SnapshotId'])

# Function to delete snapshots older than retention period
def delete_ebs_snapshot():
    retention_date = datetime.now() - timedelta(days=retention_period)

    snapshots = ec2.describe_snapshots(Filters=[{
        'Name': 'volume-id',
        'Values': [volume_id]
    }])['Snapshots']

    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        snapshot_date = snapshot['StartTime'].replace(tzinfo=None)
        if snapshot_date < retention_date:
            print(f"Deleting snapshot {snapshot_id}")
            ec2.delete_snapshot(SnapshotId=snapshot_id)

create_ebs_snapshot()
delete_ebs_snapshot()