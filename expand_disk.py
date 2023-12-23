import boto3, subprocess, os, time

def lambda_handler(event, context):
    # Setting adjustable parameters
    MULTIPLIER = 1.1
    THRESHOLD = 80
    AWS_REGION = "us-east-1"
    TOKEN = subprocess.check_output(['curl', '-X', 'PUT', 'http://169.254.169.254/latest/api/token', '-H', 'X-aws-ec2-metadata-token-ttl-seconds: 21600']).decode('utf-8')

    # Check Disk Usage
    current_usage = subprocess.check_output(['df', '-h', '/']).decode('utf-8').split('\n')[1].split()[4]
    current_usage = int(current_usage[:-1]) # Remove the percent and conveting to int

    # Condition to expand disk
    if current_usage > THRESHOLD:
        print(f"Disk usage is above {THRESHOLD}%, Expanding disk....")

        #GET instance ID
        instance_id = subprocess.check_output(['curl', '-H', f'X-aws-ec2-metadata-token: {TOKEN}', '-s', 'http://169.254.169.254/latest/meta-data/instance-id/']).strip()

        # GET volume ID
        ec2 = boto3.resource('ec2', region_name=AWS_REGION)
        instance = ec2.Instance(instance_id)
        volumes = list(instance.volumes.all())

        if not volumes:
            print("No volumes attached to the instance.")
            return
        
        volume_id = volumes[0].id

        def wait_for_volume_completion(ec2_client, volume_id):
            while True:
                volume_status = ec2_client.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]['State']

                if volume_status == 'completed':
                    break

            time.sleep(10)  # Adjust the sleep duration based on your preference

        # AWS CLI command for getting the current volume size
        ec2_client = boto3.client('ec2', region_name=AWS_REGION)
        current_size = ec2_client.describe_volumes(Volume_Ids=[volume_id])[0]['Size']

        # Calculate the new size
        new_size = int(current_size * MULTIPLIER)

        # AWS CLI command for resizing the EBS volume
        ec2_client.modify_volume(VolumeId=volume_id, Size=new_size)

        # Wait for volume modification to complete
        wait_for_volume_completion(ec2_client, volume_id)

        # Getting Disk name and Filesystem Type
        disk_name = subprocess.check_output(['lsblk', '--output', 'NAME,FSTYPE', '--noheadings']).decode('utf-8').split()[1]
        try:
            fs_type = subprocess.check_output(['lsblk', '-o', 'FSTYPE', f"/dev/{disk_name}", '--noheadings']).decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            fs_type = None

        # Resizing the partition & filesystem based on the fstype
        if fs_type == 'xfs':
            subprocess.run(['sudo', 'growpart', f'/dev/{disk_name}', '1'])
            subprocess.run(['sudo', 'xfs_growfs', '-d', '/'])
        elif fs_type == 'ext4':
            subprocess.run(['sudo', 'growpart', f'/dev/{disk_name}', '1'])
            subprocess.run(['sudo', 'resize2fs', f'/dev/{disk_name}1'])

        print("Disk expansion complete.")