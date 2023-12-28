#!/bin/bash
 
# Retrieve the Token
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
 
# Retrieve the EC2 instance ID
INSTANCE_ID=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/instance-id)
 
# Retrieve disk usage percentage
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | cut -d'%' -f1)
 
# Publish metric to CloudWatch
aws cloudwatch put-metric-data --namespace DiskUsage --metric-name DiskUsagePercentage --dimensions InstanceId=$INSTANCE_ID --value $DISK_USAGE