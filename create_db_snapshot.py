# Import necessary modules
import boto3
from datetime import datetime

# Create an console resource
aws_console = boto3.session.Sesion(profile_name="default")

# Create a RFS client
rds = aws_console.client(service_name="rds", region_name="us-east-1")

# Setting up RDS settings
rds_instance_name = ""
rds_prefix = 'automated snapshot'
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# Taking RDS snapshot
def take_rds_snapshot():
    try:
        rds_snapshot = rds.create_db_snapshot(
            DBSnapshotIdentifier=f"{rds_prefix}-{timestamp}",
            DBInstanceIdentifier=rds_instance_name
        )
        print(f"Snapshot {rds_snapshot['DBSnapshot']['DBSnapshotIdentifier']} created successfully.")
    except Exception as e:
        print(f"An error occured: {e}")

if __name__ == "__main__":
    take_rds_snapshot()