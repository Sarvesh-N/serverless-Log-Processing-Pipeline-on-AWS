import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

DYNAMODB_TABLE = "log-processing-db"
SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:329268624904:log-processing-topic"

table = dynamodb.Table(DYNAMODB_TABLE)

def lambda_handler(event, context):
    
    for record in event['Records']:
        log_message = record['body']
        
        log_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Simple analysis condition
        status = "ERROR" if "ERROR" in log_message.upper() else "INFO"
        
        # Store in DynamoDB
        table.put_item(
            Item={
                "log_id": log_id,
                "message": log_message,
                "status": status,
                "timestamp": timestamp
            }
        )
        
        # Send SNS alert if ERROR
        if status == "ERROR":
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="Log Error Alert",
                Message=f"Error detected:\n\n{log_message}"
            )
    
    return {
        "statusCode": 200,
        "body": json.dumps("Messages processed successfully")
    }