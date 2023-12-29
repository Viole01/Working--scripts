import boto3

ec2 = boto3.client('ec2')

def start_instances(instance_ids):
    ec2.start_instances(InstanceIds=instance_ids)
    print('Instances started:', instance_ids)

def stop_instances(instance_ids):
    ec2.stop_instances(InstanceIds=instance_ids)
    print('Instances stopped:', instance_ids)

def lambda_handler(event, context):

    # Specify the resource type and tag key-value pair
    resource_type = 'instance'

    tag_value_start = 'Auto-Start'
    response_start = ec2.describe_tags(Filters=[{'Name': 'resource-type', 'Values': [resource_type]}, 
                                                {'Name': 'value', 'Values': [tag_value_start]}])
    
    instances_to_start = [tag['ResourceId'] for tag in response_start.get('Tags', [])]

    if instances_to_start:
        start_instances(instances_to_start)

    tag_value_stop = 'Auto-Stop'
    response_stop = ec2.describe_tags(Filters=[{'Name': 'resource-type', 'Values': [resource_type]}, 
                                               {'Name': 'value', 'Values': [tag_value_stop]}])
    
    instances_to_stop = [tag['ResourceId'] for tag in response_stop.get('Tags', [])]

    if instances_to_stop:
        stop_instances(instances_to_stop)
