import boto3
from datetime import datetime, timedelta

# Initializw aws console session
aws_console = boto3.session.Session(profile_name="default")

# Initialize boto3 clients for CloudWatch and SNS
cloudwatch_client = aws_console.client(service_name='cloudwatch')
sns_client = aws_console.client(service_name='sns')

# Specify the CloudWatch metric and threshold
metric_name = 'EstimatedCharges'
namespace = 'Praj-AWS/Billing'
threshold_amount = 50.0

# Specify the SNS topic ARN to which the alert will be sent
sns_topic_arn = 'arn:aws:sns:us-east-1:295397358094:sns_for_cost_threshold:dc91881d-de60-4cb2-834d-828d1843da41'

def get_billing_metric():
    # Retrieve the AWS billing metric from CloudWatch
    response = cloudwatch_client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'Currency',
                'Value': 'USD'
            }
        ],
        StartTime=datetime.utcnow() - datetime.timedelta(days=1),
        EndTime= datetime.utcnow(),
        Period=86400,
        Statistics=['Maximum']
    )

    # Extract the metric value
    metric_value = response['Datapoints'][0]['Maximum']

    return metric_value

def send_sns_notification():
    # Send an SNS notification
    message = f"AWS billing has exceeded the threshold. Current billing amount: ${billing_amount}"
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject="AWS Billing Alert"
    )

def log_message(message):
    # Print messages for logging purposes
    print(f"{datetime.datetime.utcnow()} - {message}")

if __name__ == "__main__":
    # Retrieve the AWS billing metric from CloudWatch
    billing_amount = get_billing_metric()

    # Compare the billing amount with the threshold
    log_message(f"Current billing amount: ${billing_amount}")
    if billing_amount > threshold_amount:
        log_message("Billing exceeds the threshold. Sending SNS notification.")
        send_sns_notification()
    else:
        log_message("Billing is below the threshold. No action required.")
