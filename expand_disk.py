import boto3, requests, time, subprocess

def get_instance_id():
    try:
        response = requests.get('http://169.254.169.254/latest/meta-data/instance-id', timeout=2)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to fetch instance ID - {e}")
        return None

def wait_for_volume_completion(ec2_client, volume_id):
    while True:
        volume_status = ec2_client.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]['State']

        if volume_status == 'completed':
            break

        time.sleep(10)

def resize_volume(ec2_client, volume_id, new_size_gb):
    ec2_client.modify_volume(VolumeId=volume_id, Size=new_size_gb)

def main():
    # Setting adjustable parameters
    MULTIPLIER = 1.1
    THRESHOLD = 80
    AWS_REGION = "us-east-1"

    # Get the instance ID dynamically
    instance_id = get_instance_id()
    
    if not instance_id:
        print("Error: Unable to determine instance ID. Exiting.")
        return
    # No use of token as the script is running inside the instance itself...
    # TOKEN = subprocess.check_output(['curl', '-X', 'PUT', 'http://169.254.169.254/latest/api/token', '-H', 'X-aws-ec2-metadata-token-ttl-seconds: 21600']).decode('utf-8')

    # GET volumes
    ec2 = boto3.resource('ec2', region_name=AWS_REGION)
    instance = ec2.Instance(instance_id)
    volumes = list(instance.volumes.all())

    if not volumes:
        print("No volumes attached to the instance.")
        return

    # Loop through all volumes
    for volume in volumes:
        volume_id = volume.id

        # AWS CLI command for getting the current volume size
        ec2_client = boto3.client('ec2', region_name=AWS_REGION)
        current_size = ec2_client.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]['Size']

        # Check Disk Usage for the current volume
        current_usage = subprocess.check_output(['df', '-h', f'/dev/{volume.attachments[0]["Device"]}', '--output=pcent']).decode('utf-8').strip()
        current_usage = int(current_usage[:-1])  # Remove the percent and convert to int

        # Condition to expand disk
        if current_usage > THRESHOLD:
            print(f"Disk usage for volume {volume_id} is above {THRESHOLD}%, expanding disk...")

            # Calculate the new size
            new_size = int(current_size * MULTIPLIER)

            # AWS CLI command for resizing the EBS volume
            resize_volume(ec2_client, volume_id, new_size)

            # Wait for volume modification to complete
            wait_for_volume_completion(ec2_client, volume_id)

            print(f"Disk expansion for volume {volume_id} complete.")
        else:
            print(f"Disk usage for volume {volume_id} is below {THRESHOLD}%, no need to expand the disk.")

    print("All disk expansions complete.")

if __name__ == "__main__":
    main()
