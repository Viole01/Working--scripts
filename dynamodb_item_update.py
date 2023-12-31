import boto3, json, logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize aws console session
aws_console = boto3.session.Session(profile_name='default', region_name='us-east-1')

# Initialize Boto3 clients
dynamodb = aws_console.client(service_name='dynamodb')
sns = aws_console.client(service_name='sns')

def lambda_handler(event, context):
    # Process DynamoDB stream records
    for record in event['Records']:
        # Check if the record contains an update
        if record['eventName'] == 'MODIFY':
            # Extract modified item
            modified_item = record['dynamodb']['NewImage']
            
            # Convert DynamoDB JSON to Python dictionary
            modified_item_dict = {key: list(value.values())[0] for key, value in modified_item.items()}
            
            # Log the modified item
            logger.info(f"Modified Item: {json.dumps(modified_item_dict)}")

            # Send SNS notification
            sns_topic_arn = 'arn:aws:sns:us-east-1:295397358094:sns_for_cost_threshold:dc91881d-de60-4cb2-834d-828d1843da41'
            subject = 'DynamoDB Item Update'
            message = f"Modified Item: {json.dumps(modified_item_dict)}"
            
            sns.publish(TopicArn=sns_topic_arn, Subject=subject, Message=message)
            
            # Log the SNS notification
            logger.info(f"SNS notification sent for DynamoDB update: {json.dumps(modified_item_dict)}")

    return {
        'statusCode': 200,
        'body': json.dumps('Processing completed successfully!')
    }
