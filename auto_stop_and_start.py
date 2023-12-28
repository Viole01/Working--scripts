import boto3

ec2 = boto3.client('ec2')

# Function to start instances
def start_instances(instance_ids):
    ec2.start_instances(InstanceIds=instance_ids)
    print('Instances started:', instance_ids)

# Function to stop instances
def stop_instances(instance_ids):
    ec2.stop_instances(InstanceIds=instance_ids)
    print('Instances stopped:', instance_ids)

def main():
    # Specify the resource type and tag key-value pair
    resource_type = 'instance'

    tag_value = 'Auto-Start'
    response_start = ec2.describe_tags(Filters=[{'Name': 'resource-type', 'Values': [resource_type]}, 
                                                {'Name': 'value', 'Values': [tag_value]}])
    
    # Extracting the instance IDs with tag value "Auto-Start"
    instances_to_start = [tag['ResourceId'] for tag in response_start['Tags']]

    # Start the instances
    if instances_to_start:
        start_instances(instances_to_start)

    tag_value = 'Auto-Stop'
    response_stop = ec2.describe_tags(Filters=[{'Name': 'resource-type', 'Values': [resource_type]}, 
                                               {'Name': 'value', 'Values': [tag_value]}])
    
    # Extracting the instance IDs with tag value "Auto-Stop"
    instances_to_stop = [tag['ResourceId'] for tag in response_stop['Tags']]

    # Stop the instances
    if instances_to_stop:
        stop_instances(instances_to_stop)

if __name__ == '__main__':
    main()