# serverless-Log-Processing-Pipeline-on-AWS
Flow: Logs uploaded to S3 trigger a Lambda function, which pushes messages to SQS. A second Lambda analyzes each log entry, stores all logs in DynamoDB, and sends SNS alerts only when an ERROR is detected.
