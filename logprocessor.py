import json
import boto3

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

QUEUE_URL = "https://sqs.ap-south-1.amazonaws.com/329268624904/log-processing-sqs"

def lambda_handler(event, context):
    
    # Get bucket and file details from S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Read file from S3
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    file_content = response['Body'].read().decode('utf-8')
    
    # Process each line
    lines = file_content.splitlines()
    
    for line in lines:
        if line.strip() != "":
            sqs.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=line
            )
    
    return {
        "statusCode": 200,
        "body": json.dumps("File processed and messages sent to SQS")
    }